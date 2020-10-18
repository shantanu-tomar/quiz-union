from django.shortcuts import render, get_object_or_404, redirect
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.decorators import login_required
import json, random

from .models import Category, Quiz, Question, AnsweredQuestion
from .models import DIFFICULTY as difficulties
from users.models import Profile

API_CONFIG_URL = "https://opentdb.com/api_config.php"
QUIZ_BASE_URL = "https://opentdb.com/api.php?amount={}&category={}&difficulty={}&type=multiple"

def home(request):

    context = {

    }

    return render(request, "quiz/home.html", context)


# Keeping quiz categories up-to-date
def update_categories(request):
    try:
        response = requests.get(API_CONFIG_URL)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')

        categories_select = soup.find(attrs={"name": "trivia_category"})
        categories_options = categories_select.find_all('option')

        quiz_categories = []

        """Constructing a list of ( value, name ) tuple for categories.
        This list will be used to -

        Construct Category Model instances for each category (if not already present).
        This keeps the local categories up-to-date with Open Trivia.
        Category model can also be used by the Admin to create custom categories that will
        be shown to the user alongwith the categories fetched here from Open Trivia."""

        for category_tag in categories_options:
            quiz_categories.append(
                ( category_tag['value'], category_tag.text )
            )
        
        for category in quiz_categories:
            try:
                Category.objects.create(category=category[1], identifier=category[0])

            except ValidationError:
                pass

    except requests.ConnectionError:
        messages.error(request, "Connection Error! Please check your internet connection.")
        pass

    except requests.Timeout:
        messages.error(request, "Request Timeout! Please try again.")
        pass

    return redirect('quiz')


def fetch_quiz(category, difficulty, amount):
    if category == "any":
        category = ""

    api_url = QUIZ_BASE_URL.format(amount, category, difficulty)
    print(api_url)
    quiz_data = requests.get(api_url).json()
    return quiz_data


@login_required
def quiz(request):
    if request.method == 'GET':
        context = {
            "categories": Category.objects.all(),
            "difficulties": difficulties,
        }
        
        return render(request, "quiz/quiz.html", context)

    elif request.method == 'POST':
        user = request.user
        category = request.POST.get("category")
        difficulty = request.POST.get("difficulty")

        category_obj = get_object_or_404(Category, identifier=category)

        # Initiate a Quiz model instance
        user_quiz = Quiz.objects.create(
            taken_by=user, difficulty=difficulty, category=category_obj
        )


        # Checking if selected category is a custom category
        is_custom_category = category_obj.custom_category

        # If this is a custom category, questions will NOT be fetched from API, but from DB
        if is_custom_category:
            questions_qs = Question.objects.filter(category=category_obj)

            # Choosing random questions from queryset
            questions = random.sample(questions_qs, settings.QUESTION_AMOUNT)

            user_quiz.questions.add(questions)

        else:
            quiz_data = fetch_quiz(category, difficulty, settings.QUESTION_AMOUNT)

            for ques in quiz_data['results']:
                try:
                    ques_category = Category.objects.get(category=ques['category'])
                    question_obj, created = Question.objects.get_or_create(
                        question_text=ques['question'],
                        correct_answer=ques['correct_answer'], 
                        choice_2=ques['incorrect_answers'][0],
                        choice_3=ques['incorrect_answers'][1],
                        choice_4=ques['incorrect_answers'][2],
                        category=ques_category,
                        difficulty=ques['difficulty']
                    )

                    user_quiz.questions.add(question_obj)

                except ValidationError as e:
                    pass

            user_quiz.save()
        
        context = {
            "categories": Category.objects.all(),
            "difficulties": difficulties,
            "quiz": user_quiz,
        }

        return render(request, 'quiz/quiz.html', context)


@login_required
def submit_quiz(request):
    user = request.user
    quiz_id = int(request.POST.get("quiz"))
    answer_records = request.POST.get("user_answers")

    answer_records = json.loads(answer_records)
    user_profile = get_object_or_404(Profile, user=user)
    attempted_questions = len(answer_records.keys())

    # Saving user answers
    if attempted_questions > 0:
        correct_answers = 0
        incorrect_answers = 0

        for key in answer_records.keys():
            question_id = int(key)
            question = get_object_or_404(Question, id=question_id)

            if answer_records[key][1] == "True":
                answer_status = 'c'
                correct_answers += 1
            else:
                answer_status = 'w'
                incorrect_answers += 1

            record, created = AnsweredQuestion.objects.get_or_create(
                question=question, answerer=user,
                user_answer=answer_records[key][0],
                answer_status=answer_status
            )

            user_profile.attempted_questions.add(record)
            user_profile.save()

    else:
        pass

    quiz_obj = get_object_or_404(Quiz, id=quiz_id)
    quiz_obj.score = correct_answers
    quiz_obj.category = correct_answers
    quiz_obj.save()


    context = {
        "total_questions": settings.QUESTION_AMOUNT,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers
    }
    
    return render(request, 'quiz/finish.html', context)

