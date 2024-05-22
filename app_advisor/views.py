import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app_user.forms import QuestionnaireForm
from echoInvestFinal import settings
from .utils import main, plot_pie_chart


@login_required
def questionnaire(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            user_responses = form.cleaned_data
            initial_investment = user_responses.pop('initial_investment')

            # Assuming 'main' takes the current user, their responses, and initial investment as arguments
            results = main(request.user, user_responses, initial_investment)

            plot_pie_chart(results['allocated_portfolio']['region_allocation'], 'Regional Allocation',
                           'region_allocation.png')
            plot_pie_chart(results['allocated_portfolio']['sector_allocation'], 'Sector Allocation',
                           'sector_allocation.png')

            return render(request, 'portfolio/results.html', {
                'risk_score': results['risk_score'],
                'risk_tolerance': results['risk_tolerance'],
                'allocated_portfolio': results['allocated_portfolio'],
                'portfolio_performance': results['portfolio_performance'],
                'region_allocation_chart': os.path.join(settings.MEDIA_URL, 'region_allocation.png'),
                'sector_allocation_chart': os.path.join(settings.MEDIA_URL, 'sector_allocation.png')
            })
    else:
        form = QuestionnaireForm()

    return render(request, 'portfolio/questionnaire.html', {'form': form})

@login_required
def results(request):
    return render(request, 'portfolio/results.html')

@login_required
def landing(request):
    return render(request, 'portfolio/landing.html')