from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Rating(models.Model):
    id = models.IntegerField(primary_key=True, db_column='rating_id')
    distribution = models.CharField(max_length=20)
    amount_of_votes = models.IntegerField()
    rating = models.FloatField()

    class Meta:
        db_table = "rating"

    def __str__(self):
        return self.id

