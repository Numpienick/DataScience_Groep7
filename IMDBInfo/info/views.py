from django.shortcuts import render
from .models import Post, Rating


def home(request):
    context = {
        'posts': Post.objects.all(),
        'ratings': Rating.objects.all()
    }
    return render(request, 'info/home.html', context)


def about(request):
    return render(request, 'info/about.html', {'title': 'About'})
