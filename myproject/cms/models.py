from django.db import models

# Create your models here.
class Pages(models.Model):
    name = models.CharField(max_length=32, unique=True)
    page = models.TextField()
    def __str__(self):
        return self.name
