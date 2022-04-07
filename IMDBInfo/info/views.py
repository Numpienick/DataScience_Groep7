from django.shortcuts import render
from .models import Rating


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

    queryset = Rating.objects.all()
    for rating in queryset:
        labels.append(rating.id)
        data.append(rating.rating)

    return render(request, 'info/chart.html', {
        'labels': labels,
        'data': data,
    })


def rscript(request):
    return render(request, 'info/rscript.html', {'title': 'rscript'})


def hypothese(request):
    return render(request, 'info/hypothese.html', {'title': 'hypothese'})