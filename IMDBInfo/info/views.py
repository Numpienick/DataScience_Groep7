from django.shortcuts import render
# from .models import Rating
from django.db import connection


def home(request):
    return render(request, 'info/home.html')


def data(request):
    context = {
        'ratings': Rating.objects.all()
    }
    return render(request, 'info/data.html', context)


def chart(request):
    labels = []
    data = []

    cursor = connection.cursor()
    cursor.execute("SELECT rating FROM rating WHERE rating IS NOT NULL GROUP BY rating")
    data = cursor.fetchall()
    # queryset = Rating.objects.all()
    test = ''.join(data)
    for rating in data:
        # labels.append(rating.id)
        test.append(rating)

    return render(request, 'info/chart.html', {
        'labels': labels,
        'data': test,
    })


def rscript(request):
    return render(request, 'info/rscript.html', {'title': 'rscript'})


def hypothese(request):
    return render(request, 'info/hypothese.html', {'title': 'hypothese'})