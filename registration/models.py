from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    spam_likelihood = models.BooleanField(default=False)

    def __str__(self):
        return self.name
