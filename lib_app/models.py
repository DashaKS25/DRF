from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=64, unique=True)
    age = models.IntegerField(default=30)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"book - {self.title} author = {self.authors}"

