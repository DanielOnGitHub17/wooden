from django.db import models

# Create your models here.
class Player(models.Model):
    fullname = models.CharField(maxlength=200)
    email = models.EmailField()
    username = models.CharField(maxlength=30, pk=True)
    password = models.CharField(maxlength=50)
    game = models.TextField() # json text, I guess.
    

    def __str__(self):
        return self.fullname