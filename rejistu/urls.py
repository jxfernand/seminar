# rejistu/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('welcome/<int:registrant_id>/', views.welcome, name='welcome'),
    # path('registrant/<str:access_pass>/', views.registrant_detail, name='registrant_detail'),  # Add this line
    path('seminar_page/', views.seminar_page, name='seminar_page'),  # Add this line
    path('get-institution-quota/<int:institution_id>/', views.get_institution_quota, name='get_institution_quota'),
    path('recognize-face/', views.recognize_face_view, name='recognize_face'),
    path('webcam/', views.webcam_interface, name='webcam_interface'),
    # path('welcome/<str:access_pass>/', views.welcome, name='welcome'),
    path('registrant/<int:access_pass_id>/', views.registrant_detail, name='registrant_detail'),
    path("rejistu/error/", lambda request: render(request, "error_page.html"), name="error_page"),
]