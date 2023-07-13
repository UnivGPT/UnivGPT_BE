from django.urls import path
from .views import CategoryListView, CategoryDetailView

app_name = 'tag'
urlpatterns = [
    path("", CategoryListView.as_view()),
    path("<int:tag_id>/", CategoryDetailView.as_view())
]