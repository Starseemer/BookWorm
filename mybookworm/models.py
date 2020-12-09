from django.db import models


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    subtitle = models.TextField()
    price = models.CharField(max_length=15)
    url = models.URLField()
    def __str__(self):
        return "ID: " + str(self.id) + " Title: " + self.title