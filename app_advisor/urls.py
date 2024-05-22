from django.urls import path
from . import views
from .views import questionnaire, check_job_status, post_process_allocation


urlpatterns = [
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('results/', views.results, name='results'),
    path('landing/', views.landing, name='landing'),
    path('job_status/<str:job_id>/', check_job_status, name='check_job_status'),
    path('post_process/<str:job_id>/', post_process_allocation, name='post_process_allocation'),
]

