from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Rating(models.Model):
    id = models.IntegerField(primary_key=True, db_column='rating_id')
    distribution = models.CharField(max_length=20)
    amount_of_votes = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        db_table = "rating"

    def __str__(self):
        return self.id


class Country(models.Model):
    name = models.CharField(max_length=30)


class City(models.Model):
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    population = models.PositiveIntegerField()