from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Quiz, Question, AnsweredQuestion, Category
from django import forms


class QuizForm(forms.ModelForm):
    model = Quiz

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('questions').count() != 10:
            raise ValidationError(
                'You must add 10 questions in total to the quiz!'
            )


class AnsweredQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'answerer')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(AnsweredQuestion, AnsweredQuestionAdmin)