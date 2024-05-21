from django.urls import path
from . import views

urlpatterns = [
    path('allocate-portfolio/', views.AllocatePortfolioView.as_view(), name='allocate_portfolio'),
]

