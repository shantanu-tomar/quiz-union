from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from quiz import views
from users import views as user_views


urlpatterns = [
    path('', include('quiz.urls')),

    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('demo-login/', user_views.demo_login, name='demo_login'),
    path('logout/', user_views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', user_views.user_create, name='signup'),

    path("profile", include('users.urls'), name="profile"),
    # path('signup/', user_views.signup, name='signup'),

    path('admin/', admin.site.urls),
        path('password-reset/',
         auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html'), name="password_reset"),
    path('password-reset/done',
         auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'), name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'),
         name="password_reset_complete"),

]

# By default, Django doesn’t serve media files during development. Fixing it.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "The Quiz Union"
admin.site.site_title = "Quiz Union Admin Portal"
admin.site.index_title = "Welcome to the Quiz Union Administration Portal"
