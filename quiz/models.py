from django.db import models
from django.contrib.auth import get_user_model
import random, json

User = get_user_model()

DIFFICULTY = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)

ANSWER_STATUSES = (
    ('c', 'Correct'),
    ('w', 'Wrong'),
)


class ValidatedModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.clean_fields()      # validate individual fields
        self.clean()             # validate constraints between fields
        self.validate_unique()   # validate uniqueness of fields
        return super(ValidatedModel, self).save(*args, **kwargs)


class Category(ValidatedModel):
    """ Category can either be created by admin or be fetched from Open Trivia API."""
    category = models.CharField(max_length=60, unique=True)
    identifier = models.CharField(
        help_text="Identifier used in URL query parameters", max_length=10, unique=True
    )
    custom_category = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Categories'


class Question(ValidatedModel):
    """A question can either be created by admin or be fetched from Open Trivia API.
    Using TextField instead of CharField because max-length is unknown.
    """

    question_text = models.TextField()
    correct_answer = models.TextField()
    choice_2 = models.TextField()
    choice_3 = models.TextField()
    choice_4 = models.TextField()

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.CharField(choices=DIFFICULTY, max_length=6)

    def __str__(self):
        return str(self.id)

    def get_choices(self):
        choices = [
            [self.correct_answer, "True"], [self.choice_2, "False"],
            [self.choice_3, "False"], [self.choice_4, "False"],
        ]
        choices = [[x[0].replace("'", "\\'"), x[1]] for x in choices]
        random.shuffle(choices)
        return choices


class AnsweredQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answerer = models.ForeignKey(User, on_delete=models.CASCADE)
    user_answer = models.TextField()
    answer_status = models.CharField(choices=ANSWER_STATUSES, max_length=1)

    def __str__(self):
        return str(self.id)


class Quiz(models.Model):
    # Quiz is instantly generated based on difficulty & category chosen

    taken_by = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.CharField(
        choices=DIFFICULTY, max_length=6, null=True, blank=True
    )
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    questions = models.ManyToManyField(Question)
    score = models.CharField(max_length=3, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Quizzes'
