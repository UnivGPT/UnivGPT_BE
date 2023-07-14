from django.urls import path

from .views import InputDetailView, InputListView

app_name = 'input'
urlpatterns = [
    path("", InputListView.as_view()),
    # path("<int:input_id>/", InputDetailView.as_view())
    path("<int:input_id>/", InputDetailView.as_view())
]
