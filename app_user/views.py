from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy


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
    next_page = reverse_lazy('home_main')

    def form_valid(self, form):
        # Authenticate and login the user
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
