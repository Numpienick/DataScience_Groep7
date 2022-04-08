import random

from django.shortcuts import render
# from .models import Rating
from django.db import connection

from .models import vraag1SQL, vraag2SQL, vraag3SQL, vraag4SQL, vraag5SQL


def home(request):
    return render(request, 'info/home.html')


def data(request):
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


def charts(request):
    with connection.cursor() as cur:
        cur.execute("""
        SELECT genre.genre_name, count(*)
        FROM show_info
        INNER JOIN show_info_genre ON show_info.show_info_id = show_info_genre.show_info_id
        INNER JOIN genre ON show_info_genre.genre_id = genre.genre_id
        WHERE show_info.release_year = 2016
        GROUP BY show_info.release_year, genre.genre_name HAVING count(*) > 5
        """)
        fetched = cur.fetchall()
    genre_colors = []
    genres = []
    genre_data = []
    for fetch in fetched:
        genre = fetch[0]
        number = fetch[1]
        if genre not in genres:
            genres.append(genre)
        genre_data.append(number)
        r = hex(random.randrange(0, 255))[2:]
        g = hex(random.randrange(0, 255))[2:]
        b = hex(random.randrange(0, 255))[2:]
        random_col = '#' + r + g + b
        genre_colors.append(random_col)

    country_colors = []
    country_labels = []
    country_data = []
    with connection.cursor() as cur:
        cur.execute("SELECT country.country_name, COUNT(show_info.show_info_id) as count "
                       "FROM show_info "
                       "LEFT JOIN rating ON show_info.rating_id = rating.rating_id "
                       "LEFT JOIN show_info_country ON show_info.show_info_id = show_info_country.show_info_id "
                       "LEFT JOIN country ON show_info_country.country_id = country.country_id "
                       "WHERE rating.rating > 8 AND country.country_name IS NOT NULL "
                       "GROUP BY country.country_name HAVING COUNT(show_info.show_info_id) > 100")
        returned_data = cur.fetchall()

    for country in returned_data:
        r = hex(random.randrange(0, 255))[2:]
        g = hex(random.randrange(0, 255))[2:]
        b = hex(random.randrange(0, 255))[2:]

        random_col = '#' + r + g + b
        country_colors.append(random_col)
        country_labels.append(country[0])
        country_data.append(country[1])

    with connection.cursor() as cur:
        cur.execute("""
        SELECT show_info.release_year, genre.genre_name, count(*) as amount
        FROM show_info
        INNER JOIN show_info_genre ON show_info.show_info_id = show_info_genre.show_info_id
        INNER JOIN genre ON show_info_genre.genre_id = genre.genre_id
        INNER JOIN rating ON show_info.rating_id = rating.rating_id
        WHERE rating.amount_of_votes > 20 AND show_info.release_year BETWEEN 2010 AND 2016
        GROUP BY show_info.release_year, genre.genre_name HAVING count(*)> 5
        """)
        fetched = cur.fetchall()

    yearly_data = []
    years = []
    for genre in genres:
        r = hex(random.randrange(0, 255))[2:]
        g = hex(random.randrange(0, 255))[2:]
        b = hex(random.randrange(0, 255))[2:]
        random_col = '#' + r + g + b
        yearly_data.append({
            "label": genre,
            "backgroundColor": "rgba(0,0,0,0)",
            "borderColor": random_col,
            "pointBackgroundColor": "rgb(0,0,0)",
            "data": []

        })
    count = 0
    for fetch in fetched:
        year = fetch[0]
        genre = fetch[1]
        amount = fetch[2]
        if year not in years:
            years.append(year)
        for dataset in yearly_data:
            if ("label", genre) in dataset.items():
                dataset["data"].append({
                    "x": f"{year}",
                    "y": amount

                })
                count += 1

    data = {
        'genre_data': genre_data,
        'genre_labels': genres,
        'country_data': country_data,
        'country_labels': country_labels,
        'genre_colors': genre_colors,
        'country_colors': country_colors,
        'yearly_data': yearly_data,
        'years': years
    }

    return render(request, 'info/chart.html', data)


def rscript(request):
    return render(request, 'info/rscript.html', {'title': 'rscript'})


def hypothese(request):
    return render(request, 'info/hypothese.html', {'title': 'hypothese'})