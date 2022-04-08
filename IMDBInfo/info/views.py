import random

from django.shortcuts import render
# from .models import Rating
from django.db import connection
from django_tables2 import tables

from .models import Simple, vraag1SQL, vraag2SQL, vraag3SQL, vraag4SQL, vraag5SQL


class SimpleTable(tables.Table):
    class Meta:
        model = Simple

class TableView(tables.Table):
    table_class = SimpleTable
    queryset = Simple.objects.all()
    template_name = "data.html"


def home(request):
    return render(request, 'info/home.html')


def data(request):
    # cursor = connection.cursor()
    # cursor.execute("SELECT role.first_name, role.last_name, role.nick_name, COUNT(show_info.show_info_id) "
    #                "FROM role "
    #                "INNER JOIN show_info ON role.show_info_id = show_info.show_info_id "
    #                "INNER JOIN rating ON show_info.rating_id = rating.rating_id "
    #                "WHERE rating.rating < 8"
    #                "GROUP BY role.first_name, role.last_name, role.nick_name LIMIT 10")
    # returned_data = cursor.fetchall()

    context = {
        'vraag1SQL': vraag1SQL.objects.raw("SELECT role.first_name, role.last_name, role.nick_name, COUNT(show_info.show_info_id) AS amount "
                                           "FROM role "
                                           "INNER JOIN show_info "
                                           "ON role.show_info_id = show_info.show_info_id "
                                           "INNER JOIN rating "
                                           "ON show_info.rating_id = rating.rating_id "
                                           "WHERE rating.rating > 8 "
                                           "GROUP BY role.first_name, role.last_name, role.nick_name "
                                           "ORDER BY amount DESC LIMIT 10"),

        'vraag2SQL': vraag2SQL.objects.raw("SELECT show_info.show_title, rating.rating "
                                           "FROM Show_info "
                                           "INNER JOIN rating ON show_info.rating_id = rating.rating_id "
                                           "WHERE rating.rating > 1 "
                                           "AND rating.amount_of_votes > 100000"
                                           "ORDER BY rating.rating DESC LIMIT 10"),

        'vraag3SQL': vraag3SQL.objects.raw("SELECT role.first_name, role.last_name, role.nick_name, COUNT(show_info.show_info_id) AS amount "
                                           "FROM role "
                                           "INNER JOIN show_info "
                                           "ON role.show_info_id = show_info.show_info_id "
                                           "INNER JOIN rating "
                                           "ON show_info.rating_id = rating.rating_id "
                                           "WHERE rating.rating < 6 "
                                           "AND role.female = TRUE "
                                           "GROUP BY role.first_name, role.last_name, role.nick_name "
                                           "ORDER BY amount DESC LIMIT 50"),

        'vraag4SQL': vraag4SQL.objects.raw("SELECT genre.genre_name, COUNT(show_info_genre.genre_id) AS amount "
                                           "FROM show_info_genre "
                                           "INNER JOIN genre "
                                           "ON show_info_genre.genre_id = genre.genre_id "
                                           "GROUP BY genre.genre_name, show_info_genre.genre_id "
                                           "ORDER BY amount DESC"),

        'vraag5SQL': vraag5SQL.objects.raw("SELECT combies, COUNT(*) AS amount "
                                           "FROM ( "
                                           "SELECT array_to_string(array_agg(genre.genre_name), ',') AS combies, COUNT(*) AS comby "
                                           "FROM genre "
                                           "INNER JOIN show_info_genre "
                                           "ON genre.genre_id = show_info_genre.genre_id "
                                           "INNER JOIN show_info "
                                           "ON show_info_genre.show_info_id = show_info.show_info_id "
                                           "INNER JOIN rating "
                                           "ON show_info.rating_id = rating.rating_id "
                                           "WHERE rating.rating > 8 GROUP BY show_info_genre.show_info_id "
                                           ") genre "
                                           "WHERE  comby > 1 "
                                           "GROUP BY combies "
                                           "ORDER BY amount DESC LIMIT 50")
    }

    return render(request, 'info/data.html', context)


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