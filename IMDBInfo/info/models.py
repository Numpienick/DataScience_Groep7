from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Simple(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    nick_name = models.CharField(max_length=200)
    count = models.IntegerField()


class vraag1SQL(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    nick_name = models.CharField(max_length=200)
    amount = models.IntegerField(primary_key=True)


class vraag2SQL(models.Model):
    show_title = models.CharField(max_length=200)
    rating = models.IntegerField(primary_key=True)


class vraag3SQL(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    nick_name = models.CharField(max_length=200)
    amount = models.IntegerField(primary_key=True)


class vraag4SQL(models.Model):
    combies = models.CharField(max_length=200)
    amount = models.IntegerField(primary_key=True)


class vraag5SQL(models.Model):
    genre_name = models.CharField(max_length=200)
    amount = models.IntegerField(primary_key=True)

# class Cinematographer(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='person_id')
#     nick_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     type_of_cinematographer = models.CharField(max_length=100)
#     type_of_director = models.CharField(max_length=100)
#     segment = models.CharField(max_length=100)
#     scenes_deleted = models.CharField(max_length=100)
#     credit_only = models.BooleanField()
#     archive_footage = models.BooleanField()
#     rumored = models.BooleanField()
#
#     class Meta:
#         db_table = "cinematographer"
#
#     def __str__(self):
#         return self.id
#
#
# class Director(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='director_id')
#     person_id = models.IntegerField()
#     nick_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     type_of_director = models.CharField(max_length=100)
#     segment = models.CharField(max_length=100)
#     scenes_deleted = models.CharField(max_length=100)
#     credit_only = models.BooleanField()
#     archive_footage = models.BooleanField()
#     uncredited = models.BooleanField()
#     rumored = models.BooleanField()
#
#     class Meta:
#         db_table = "director"
#
#     def __str__(self):
#         return self.id
#
#
# class Plot(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='plot_id')
#     plot = models.CharField(max_length=255)
#     written_by = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = "plot"
#
#     def __str__(self):
#         return self.id
#
#
# class Person(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='person_id')
#     nick_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = "person"
#
#     def __str__(self):
#         return self.id
#
#
# class Rating(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='rating_id')
#     distribution = models.CharField(max_length=20, default=None, blank=True, null=True)
#     amount_of_votes = models.IntegerField(default=None, blank=True, null=True)
#     rating = models.FloatField(default=None, blank=True, null=True)
#
#     class Meta:
#         db_table = "rating"
#
#     def __str__(self):
#         return self.id
#
#
# class Show_info(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='show_info_id')
#     rating_id = models.ForeignKey(Rating, on_delete=models.CASCADE)
#     show_title = models.CharField(max_length=100)
#     release_date = models.CharField(max_length=100)
#     release_year = models.IntegerField()
#     type_of_show = models.CharField(max_length=100)
#     suspended = models.BooleanField()
#
#     class Meta:
#         db_table = "show_info"
#
#     def __str__(self):
#         return self.id
#
#
# class Role(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='role_id')
#     person_id = models.IntegerField()
#     show_info_id = models.ForeignKey(Show_info, on_delete=models.CASCADE)
#     nick_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     character_name = models.CharField(max_length=100)
#     segment = models.CharField(max_length=100)
#     voice_actor = models.CharField(max_length=100)
#     scenes_deleted = models.CharField(max_length=100)
#     credit_only = models.BooleanField()
#     archive_footage = models.BooleanField()
#     uncredited = models.BooleanField()
#     rumored = models.BooleanField()
#     motion_capture = models.CharField(max_length=100)
#     role_position = models.CharField(max_length=100)
#     female = models.BooleanField()
#
#     class Meta:
#         db_table = "director"
#
#     def __str__(self):
#         return self.id
#
#
# class Country(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='country_id')
#     country_name = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = "country"
#
#     def __str__(self):
#         return self.id
#
#
# class Running_times(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='running_times_id')
#     country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
#     running_times = models.IntegerField()
#     including_commercials = models.BooleanField()
#     festival = models.CharField(max_length=100)
#     cut = models.CharField(max_length=100)
#     market = models.CharField(max_length=100)
#     print = models.CharField(max_length=100)
#     approximated = models.BooleanField()
#     amount_of_episodes = models.CharField(max_length=100)
#     fps = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = "running_times"
#
#     def __str__(self):
#         return self.id
#
#
# class Genre(models.Model):
#     id = models.IntegerField(primary_key=True, db_column='genre_id')
#     genre_name = models.CharField(max_length=100)
#
#     class Meta:
#         db_table = "genre"
#
#     def __str__(self):
#         return self.id
#
#
# class Show_info_cinematographer(models.Model):
#     show_info_id = models.ForeignKey(Show_info, on_delete=models.CASCADE)
#     cinematographer_id = models.ForeignKey(Cinematographer, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "show_info_cinematographer"
#
#     def __str__(self):
#         return self.id
#
#
# class Show_info_country(models.Model):
#     show_info_id = models.ForeignKey(Show_info, on_delete=models.CASCADE)
#     country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "show_info_country"
#
#     def __str__(self):
#         return self.id
#
# class Show_info_director(models.Model):
#     show_info_id = models.ForeignKey(Show_info, on_delete=models.CASCADE)
#     director_id = models.ForeignKey(Director, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "show_info_director"
#
#     def __str__(self):
#         return self.id
#
#
# class Show_info_genre(models.Model):
#     show_info_id = models.ForeignKey(Show_info, on_delete=models.CASCADE)
#     genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "show_info_genre"
#
#     def __str__(self):
#         return self.id
#
# class Show_info_plot(models.Model):
#     show_info_id = models.ForeignKey(Show_info, on_delete=models.CASCADE)
#     plot_id = models.ForeignKey(Plot, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "show_info_plot"
#
#     def __str__(self):
#         return self.id
#
# class Show_info_running_times(models.Model):
#     show_info_id = models.ForeignKey(Show_info, on_delete=models.CASCADE)
#     running_times_id = models.ForeignKey(Running_times, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = "show_info_running_times"
#
#     def __str__(self):
#         return self.id
#
