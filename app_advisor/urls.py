from django.urls import path
from . import views

urlpatterns = [
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('results/', views.results, name='results'),
    path('landing/', views.landing, name='landing'),
]
