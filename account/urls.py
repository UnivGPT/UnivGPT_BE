from django.urls import path
from .views import SignupView

app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
]