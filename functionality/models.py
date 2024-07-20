from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=150)
    userid = models.IntegerField()
    publishdate = models.DateField(max_length=100, default="No publish date available")
    subtitle = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    thumbnail = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    rating = models.IntegerField(null=True, blank=True)
    started_reading = models.DateField(max_length=100)
    ended_reading = models.DateField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title
    
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    readbooks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
