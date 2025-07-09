from django.urls import path
from . import views

urlpatterns = [
    path("", views.tast_list, name="tasks")
]