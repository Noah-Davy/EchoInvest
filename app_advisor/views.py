from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app_user.forms import QuestionnaireForm
from .utils import main


@login_required
def questionnaire(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            user_responses = form.cleaned_data
            initial_investment = user_responses.pop('initial_investment')

            # Assuming 'main' takes the current user, their responses, and initial investment as arguments
            results = main(request.user, user_responses, initial_investment)

            return render(request, 'portfolio/results.html', {
                'risk_score': results['risk_score'],
                'risk_tolerance': results['risk_tolerance'],
                'allocated_portfolio': results['allocated_portfolio'],
                'portfolio_performance': results['portfolio_performance']
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