from django.db import models

# Create your models here.
class Player(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.EmailField()
    username = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.fullname