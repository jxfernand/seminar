from django.db import models

class Registrant(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='registrant_photos/')

    def __str__(self):
        return self.name
