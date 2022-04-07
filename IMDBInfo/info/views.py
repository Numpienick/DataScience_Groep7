from django.shortcuts import render
# from .models import Rating
from django.db import connection


def home(request):
    return render(request, 'info/home.html')


def data(request):
    # context = {
    #     'ratings': Rating.objects.all()
    # }
    return render(request, 'info/data.html')

def popularity_chart(request):
    with connection.cursor() as cur:
        cur.execute("""
        SELECT show_info.release_year, genre.genre_name, count(*)
        FROM show_info
        INNER JOIN show_info_genre ON show_info.show_info_id = show_info_genre.show_info_id
        INNER JOIN genre ON show_info_genre.genre_id = genre.genre_id
        WHERE show_info.release_year = 2016
        GROUP BY show_info.release_year, genre.genre_name
        """)
        fetched = cur.fetchall()
    xdata = []
    ydata = []
    genres = []
    chartdata = []
    for fetch in fetched:
        year = fetch[0]
        genre = fetch[1]
        number = fetch[2]
        if year not in xdata:
            xdata.append(year)
        if genre not in genres:
            genres.append(genre)
        if number not in ydata:
            ydata.append(number)
        chartdata.append(number)

    data = {
        'chartdata': chartdata,
        'labels': genres
    }

    return render(request, 'info/chart.html', data)

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