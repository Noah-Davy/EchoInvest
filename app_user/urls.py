from django.urls import path
from .views import register, home_view, CustomLogoutView, CustomLoginView, main_home_view, ResultsView
from .views import QuestionnaireView

urlpatterns = [
    path('register/', register, name='register'),
    path('home/', home_view, name='home'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('home_main/', main_home_view, name='home_main'),
    path('questionnaire/', QuestionnaireView.as_view(), name='questionnaire'),
    path('results/', ResultsView.as_view(), name='results'),  # Add this line

]

