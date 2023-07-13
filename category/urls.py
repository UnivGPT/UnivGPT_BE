from django.urls import path
from .views import CategoryListView, CategoryDetailView

app_name = 'category'
urlpatterns = [
    path("", CategoryListView.as_view()),
    path("<int:category_id>/", CategoryDetailView.as_view())
]
