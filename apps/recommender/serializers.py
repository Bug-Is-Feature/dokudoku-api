from rest_framework import serializers

from apps.books.models import Book

class RecommenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('__all__')