from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


STEEZY=(
    ('C', 'Cruise'),
    ('S', 'Street'),
    ('P', 'Park'),
)

# Create your models here.

class Park(models.Model):
  name = models.CharField(max_length=50)
  location = models.CharField(max_length=20)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('parks_detail', kwargs={'pk': self.id})

class Trick(models.Model):
    name=models.CharField(max_length=100)
    stance=models.CharField(max_length=100)
    description=models.TextField(max_length=250)
    dial=models.IntegerField()
    parks=models.ManyToManyField(Park)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={ 'trick_id': self.id })

    def trained_for_today(self):
        return self.training_set.filter(date=date.today()).count() >= len(STEEZY)

class Training(models.Model):
    date=models.DateField()
    steez=models.CharField(
        max_length=1,
        choices=STEEZY,
        default=STEEZY[0][0]
        )
    trick=models.ForeignKey(Trick, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.get_steez_display()} on {self.date}'
    
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url=models.CharField(max_length=200)
    trick=models.ForeignKey(Trick, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for trick_id: {self.trick_id} @{self.url}"

