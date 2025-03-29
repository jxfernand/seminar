# seminar_project/facer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('capture-and-compare/', views.capture_and_compare, name='capture_and_compare'),
]
