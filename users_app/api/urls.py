from django.urls import path
from .views import EmailCheckView, RegisterView, LoginView

urlpatterns = [
    path('registration/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('email-check/', EmailCheckView.as_view()),
]
