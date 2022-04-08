import random

from django.shortcuts import render
# from .models import Rating
from django.db import connection

def home(request):
    return render(request, 'info/home.html')


def data(request):
    labels = []
    data = []
    colors = []

    cursor = connection.cursor()
    cursor.execute("SELECT role.first_name, role.last_name, role.nick_name, COUNT(show_info.show_info_id) "
                   "FROM role "
                   "INNER JOIN show_info ON role.show_info_id = show_info.show_info_id "
                   "INNER JOIN rating ON show_info.rating_id = rating.rating_id "
                   "WHERE rating.rating > 8 "
                   "GROUP BY role.first_name, role.last_name, role.nick_name")


    returned_data = cursor.fetchall()

    context = {
        # 'ratings': Rating.objects.all()
    }

    return render(request, 'info/chart.html', data)

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
    colors = []

    cursor = connection.cursor()
    cursor.execute("SELECT country.country_name, COUNT(show_info.show_info_id) as count "
                   "FROM show_info "
                   "LEFT JOIN rating ON show_info.rating_id = rating.rating_id "
                   "LEFT JOIN show_info_country ON show_info.show_info_id = show_info_country.show_info_id "
                   "LEFT JOIN country ON show_info_country.country_id = country.country_id "
                   "WHERE rating.rating > 8 AND country.country_name IS NOT NULL "
                   "GROUP BY country.country_name HAVING COUNT(show_info.show_info_id) > 100")

    returned_data = cursor.fetchall()

    for country in returned_data:
        r = hex(random.randrange(0, 255))[2:]
        g = hex(random.randrange(0, 255))[2:]
        b = hex(random.randrange(0, 255))[2:]

        random_col = '#' + r + g + b
        colors.append(random_col)
        labels.append(country[0])
        data.append(country[1])
    return render(request, 'info/chart.html', {
        'country_labels': labels,
        'country_data': returned_data,
        'colors': colors
    })


def rscript(request):
    return render(request, 'info/rscript.html', {'title': 'rscript'})


def hypothese(request):
    return render(request, 'info/hypothese.html', {'title': 'hypothese'})