from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.seminar_page, name='seminar_page'),
   
]


