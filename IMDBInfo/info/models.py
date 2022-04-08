from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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