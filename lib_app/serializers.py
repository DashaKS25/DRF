from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_book_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title length should be at least 3 characters")
        return value
