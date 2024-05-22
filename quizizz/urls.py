from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('check_student_and_join_code/', views.check_student_and_join_code, name='check_student_and_join_code'),
    path('pre_game/', views.pre_game, name='pre_game'),
    path('countdown/', views.countdown, name='countdown'),
    path('quiz/', views.quiz, name='quiz'),
]
