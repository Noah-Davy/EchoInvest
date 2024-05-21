from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import QuestionnaireForm
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.views import View
import requests
from django.http import JsonResponse
import json




def home_view(request):
    return render(request, 'portfolio/home.html')

@login_required
def main_home_view(request):
    return render(request, 'portfolio/home_main.html')


def how_it_works(request):
    return render(request, 'portfolio/how_it_works.html')


def blog(request):
    return render(request, 'portfolio/blog.html')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'portfolio/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'portfolio/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('questionnaire')

    def form_valid(self, form):
        # Authenticate and login the user
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class QuestionnaireView(View):
    def get(self, request):
        form = QuestionnaireForm()
        return render(request, 'portfolio/questionnaire.html', {'form': form})

    def post(self, request):
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            user_responses = form.cleaned_data
            initial_investment = request.POST.get('initial_investment')

            # Prepare data for the API request
            data = {
                'user_responses': user_responses,
                'initial_investment': initial_investment
            }

            # Make a POST request to AllocatePortfolioView API endpoint
            response = requests.post(
                request.build_absolute_uri('/advisor/allocate-portfolio/'),
                headers={'Content-Type': 'application/json'},
                data=json.dumps(data)
            )

            if response.status_code == 200:
                data = response.json()
                request.session['risk_score'] = data['risk_score']
                request.session['risk_tolerance'] = data['risk_tolerance']
                request.session['recommended_portfolio'] = data['recommended_portfolio']
                request.session['allocated_portfolio'] = data['allocated_portfolio']
                request.session['portfolio_performance'] = data['portfolio_performance']
                return redirect('results')  # Redirect to the results page
            else:
                # Handle API error
                form.add_error(None, 'Error processing your request. Please try again later.')

        return render(request, 'portfolio/questionnaire.html', {'form': form})



class ResultsView(View):
    def get(self, request):
        # This data should be passed from the QuestionnaireView after processing
        context = {
            'risk_score': request.session.get('risk_score'),
            'risk_tolerance': request.session.get('risk_tolerance'),
            'recommended_portfolio': request.session.get('recommended_portfolio'),
            'allocated_portfolio': request.session.get('allocated_portfolio'),
            'portfolio_performance': request.session.get('portfolio_performance')
        }
        return render(request, 'portfolio/results.html', context)