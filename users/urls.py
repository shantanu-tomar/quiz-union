from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView

app_name = 'users'

urlpatterns = [
    path("", views.profile, name="profile"),
    path("history/", views.quiz_history, name="quiz_history"),
    path("change-password/", PasswordChangeView.as_view(
        template_name='users/password_change.html', success_url=reverse_lazy('users:password_change_done')), name='change_password'),
    
    path("change-password/done", PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'),

]

