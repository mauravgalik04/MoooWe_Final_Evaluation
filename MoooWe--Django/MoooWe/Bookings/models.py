from django.db import models
from Movies.models import AppUser, Movie
# Create your models here.
class Theatre(models.Model):
    name = models.CharField(max_length = 20)
    location = models.TextField()
    capacity = models.IntegerField()
    gold_seats = models.IntegerField()
    gold_price = models.DecimalField(decimal_places=2 , max_digits=6)
    silver_seats = models.IntegerField()
    silver_price = models.DecimalField(decimal_places=2, max_digits=6)
    bronze_seats = models.IntegerField()
    bronze_price = models.DecimalField(decimal_places = 2 , max_digits=6)
    image = models.ImageField(upload_to='Movies/static/uploads/')
    owner = models.ForeignKey(AppUser , on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Show(models.Model):
    time_choices  = (
        ('Morning' , 'Morning'),
        ('Afternoon' , 'Afternoon'),
        ('Evening' , 'Evening')
    )
    movie_name = models.CharField(max_length=50)
    duration = models.CharField(max_length=10)
    time = models.CharField(max_length=20 , choices=time_choices)
    date = models.DateField()
    movie_poster = models.ImageField(upload_to='Movies/static/uploads')
    theatre = models.ForeignKey(Theatre , on_delete= models.CASCADE)
    def __str__(self):
        return self.movie_name
    
