from django.urls import path,include
from .views import UserRegistrationView,LoginView,UserprofileView,UserChangePassword,SendPasswordResetEmailView,UserPasswordResetView


urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', UserprofileView.as_view()),
    path('changepassword/', UserChangePassword.as_view()),
    path('send-password-reset-email/', SendPasswordResetEmailView.as_view()),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view()),
]
