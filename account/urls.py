from django.urls import path
from .views import SignupView, SigninView, LogoutView, TokenRefreshView, UserInfoView, SocialLoginCallbackView, KakaoLoginCallbackView

app_name = 'account'
urlpatterns = [
    path("signup/", SignupView.as_view()),
    path("signin/", SigninView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("info/", UserInfoView.as_view()),
    path("socials/", SocialLoginCallbackView.as_view()),
    path("kakao/", KakaoLoginCallbackView.as_view())
]