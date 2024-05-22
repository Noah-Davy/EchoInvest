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

            # Generate and save charts
            plot_pie_chart(results['allocated_portfolio']['region_allocation'], 'Regional Allocation',
                           'region_allocation.png')
            plot_pie_chart(results['allocated_portfolio']['sector_allocation'], 'Sector Allocation',
                           'sector_allocation.png')

            # Check if 'spy_performance' exists in results
            if 'spy_performance' in results:
                # Combine portfolio and spy performance data for easier rendering in template
                performance_combined = [
                    {'date': date, 'portfolio_value': port_value, 'spy_value': spy_value}
                    for (date, port_value), (_, spy_value) in zip(results['portfolio_performance'], results['spy_performance'])
                ]

                return render(request, 'portfolio/results.html', {
                    'risk_score': results['risk_score'],
                    'risk_tolerance': results['risk_tolerance'],
                    'allocated_portfolio': results['allocated_portfolio'],
                    'performance_combined': performance_combined,
                    'region_allocation_chart': os.path.join(settings.STATIC_URL, 'region_allocation.png'),
                    'sector_allocation_chart': os.path.join(settings.STATIC_URL, 'sector_allocation.png')
                })
            else:
                return render(request, 'portfolio/results.html', {
                    'risk_score': results['risk_score'],
                    'risk_tolerance': results['risk_tolerance'],
                    'allocated_portfolio': results['allocated_portfolio'],
                    'performance_combined': [],
                    'region_allocation_chart': os.path.join(settings.STATIC_URL, 'region_allocation.png'),
                    'sector_allocation_chart': os.path.join(settings.STATIC_URL, 'sector_allocation.png')
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