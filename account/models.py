from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/profile', blank=True, null=True)
    email = models.EmailField(max_length=200)
    name = models.CharField(max_length=400)
    bio = models.TextField(max_length=200)

    def __str__(self):
        return f'{self.user} -- {self.image} -- {self.email}'
