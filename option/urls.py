from django.urls import path

from .views import OptionDetailView, OptionListView

app_name = 'option'
urlpatterns = [
    path("", OptionListView.as_view()),
    path("<int:option_id>/", OptionDetailView.as_view()),
]