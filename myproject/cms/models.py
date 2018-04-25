from django.db import models

# Create your models here.
class Pages(models.Model):
    name = models.CharField(max_length=32, unique=True)
    page = models.TextField()
    def __str__(self):
        return self.name

class Barrapunto(models.Model):
    title = models.TextField(unique=True)
    link = models.URLField()
    def __str__(self):
        return self.title
