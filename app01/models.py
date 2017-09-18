from django.db import models

class Author(models.Model):
    name=models.CharField(max_length=32)
    sex=models.CharField(max_length=10)
    age=models.IntegerField()
    university=models.CharField(max_length=32)

class Publish(models.Model):
    name=models.CharField(max_length=32)
    addr=models.CharField(max_length=32)

class Classify(models.Model):
    category=models.CharField(max_length=32)

class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    date = models.CharField(max_length=64)
    publish = models.ForeignKey(Publish)
    classify = models.ForeignKey(Classify)
    author = models.ManyToManyField(Author)