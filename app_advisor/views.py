import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app_user.forms import QuestionnaireForm
from echoInvestFinal import settings
from .utils import main, plot_pie_chart

import os
import time
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from app_user.forms import QuestionnaireForm
from .utils import main, calculate_portfolio_performance, generate_allocation_charts, save_portfolio, \
    get_previous_trading_day
from rq import Queue
from echoInvestFinal.worker import conn
from rq.job import Job


def questionnaire(request):
    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            user_responses = form.cleaned_data
            initial_investment = user_responses.pop('initial_investment')

            # Enqueue the main function as a background job
            results = main(request.user, user_responses, initial_investment)

            # Return job ID to the client
            return JsonResponse({'job_id': results['job_id'], 'risk_score': results['risk_score'],
                                 'risk_tolerance': results['risk_tolerance']})
    else:
        form = QuestionnaireForm()

    return render(request, 'portfolio/questionnaire.html', {'form': form})


def check_job_status(request, job_id):
    job = Job.fetch(job_id, connection=conn)
    return JsonResponse({'status': job.get_status()})


def post_process_allocation(request, job_id):
    job = Job.fetch(job_id, connection=conn)

    if job.is_finished:
        allocated_portfolio = job.result
        user = job.meta['user']
        risk_score = job.meta['risk_score']
        risk_tolerance = job.meta['risk_tolerance']
        initial_investment = job.args[1]  # Retrieve initial_investment from job args

        # Get the previous trading day
        end_date = get_previous_trading_day()

        # Calculate the portfolio performance over the last 10 years
        portfolio_performance_data = calculate_portfolio_performance(allocated_portfolio, initial_investment, end_date)

        # Generate and save allocation charts
        generate_allocation_charts(allocated_portfolio)

        # Save the portfolio to the database
        save_portfolio(user, risk_score, risk_tolerance, allocated_portfolio, portfolio_performance_data)

        # Zip the portfolio and SPY performance data
        performance_zip = list(
            zip(portfolio_performance_data['portfolio_performance'], portfolio_performance_data['spy_performance']))

        return JsonResponse({
            'status': 'finished',
            'risk_score': risk_score,
            'risk_tolerance': risk_tolerance,
            'allocated_portfolio': allocated_portfolio,
            'portfolio_performance': performance_zip
        })
    elif job.is_failed:
        return JsonResponse({'status': 'failed', 'error': str(job.exc_info)})
    else:
        return JsonResponse({'status': job.get_status()})


@login_required
def results(request):
    return render(request, 'portfolio/results.html')

@login_required
def landing(request):
    return render(request, 'portfolio/landing.html')