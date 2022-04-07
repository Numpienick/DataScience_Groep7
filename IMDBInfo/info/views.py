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
    cursor.execute("SELECT rating, COUNT(show_info.show_info_id) as count FROM show_info WHERE rating > 8 GROUP BY rating")
    returned_data = cursor.fetchall()

    for rating in returned_data:
        labels.append(rating[0])
        data.append(rating[1])
    return render(request, 'info/chart.html', {
        'labels': labels,
        'data': returned_data,
    })


def rscript(request):
    return render(request, 'info/rscript.html', {'title': 'rscript'})


def hypothese(request):
    return render(request, 'info/hypothese.html', {'title': 'hypothese'})