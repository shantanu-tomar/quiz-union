from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("quiz/", views.quiz, name="quiz"),
    path("update-categories/", views.update_categories, name="update_categories"),
    path("submit-quiz/", views.submit_quiz, name="submit_quiz"),
]