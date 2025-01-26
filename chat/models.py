from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    

class Words(models.Model):
    word = models.CharField(max_length=100)
    meaning = models.TextField()
    example = models.TextField()

    def __str__(self):
        return self.word