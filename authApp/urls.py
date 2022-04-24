from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, LoginView
from authApp import views
from django.contrib.auth import views as auth_views

app_name = 'authApp'

urlpatterns = [
    path('profile/<pk>', views.CustomUserView.as_view(), name="profile"),
    path('edit_user/<pk>', views.UserUpdateView.as_view(), name='edit_user'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='authApp/login.html'), name='login'),
    path('signup/', views.registration_view, name='signup'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='authApp/password_reset/password_change_done.html'), 
        name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='authApp/password_reset/password_change.html',
    success_url=reverse_lazy('authApp:password_change_done')), 
        name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authApp/password_reset/password_reset_done.html'),
     name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('authApp:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='authApp/password_reset/password_reset_email.html',
        subject_template_name='authApp/password_reset/password_reset_subject.txt',
        success_url=reverse_lazy('authApp:password_reset_done')
    ), name='password_reset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='authApp/password_reset/password_reset_complete.html'),
     name='password_reset_complete'),
    path('activate/(<uidb64>/<token>/', views.activate, name='activate'),
]
