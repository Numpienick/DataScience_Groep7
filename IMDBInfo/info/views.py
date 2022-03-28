from django.shortcuts import render
from .models import Post, Rating, City


def home(request):
    context = {
        'posts': Post.objects.all(),
        'ratings': Rating.objects.all()
    }
    return render(request, 'info/home.html', context)

def data(request):
    context = {
        'ratings': Rating.objects.all()
    }
    return render(request, 'info/data.html', context)

def about(request):
    return render(request, 'info/about.html', {'title': 'About'})


def pie_chart(request):
    labels = []
    data = []

    queryset = Rating.objects.all()
    for rating in queryset:
        labels.append(rating.id)
        data.append(rating.rating)

    return render(request, 'info/pie_chart.html', {
        'labels': labels,
        'data': data,
    })


def line_chart(request):
    labels = []
    data = []

    queryset = Rating.objects.all()
    for rating in queryset:
        labels.append(rating.id)
        data.append(rating.rating)

    return render(request, 'info/line_chart.html', {
        'labels': labels,
        'data': data,
    })
