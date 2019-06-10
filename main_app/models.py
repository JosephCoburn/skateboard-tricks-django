from django.db import models

# Create your models here.
class Trick(models.Model):
    name=models.CharField(max_length=100)
    stance=models.CharField(max_length=100)
    description=models.TextField(max_length=250)
    dial=models.IntegerField()

    def __str__(self):
        return self.name