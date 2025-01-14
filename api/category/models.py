from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True) #auto when created
    updated_at = models.DateTimeField(auto_now=True) #auto each time saved
    def __str__(self):
        return self.name