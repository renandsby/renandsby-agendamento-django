from django.conf.urls import include
from django.urls import path

from . import views

app_name = "tutorial"

urlpatterns = [
    path("", views.tutorial_list, name="tutorial-list"),
]
