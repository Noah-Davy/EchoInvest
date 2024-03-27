from django.shortcuts import render


def home_view(request):
    return render(request, 'portfolio/home.html')


def how_it_works(request):
    return render(request, 'portfolio/how_it_works.html')


def blog(request):
    return render(request, 'portfolio/blog.html')
