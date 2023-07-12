from django.urls import path

from .views import PromptListView, PromptDetailView

app_name = 'prompt'
urlpatterns = [
    path("", PromptListView.as_view()),
    path("<int:prompt_id>/", PromptDetailView.as_view())
]
