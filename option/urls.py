from django.urls import path

from .views import OptionDetailView, OptionListView, OptionFromInputView

app_name = 'option'
urlpatterns = [
    path("", OptionListView.as_view()),
    path("<int:option_id>/", OptionDetailView.as_view()),
    path("frominput/", OptionFromInputView.as_view())
]