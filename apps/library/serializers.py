from collections import OrderedDict
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.books.models import Author, Book
from apps.books.serializers import BookSerializer
from apps.users.models import User
from apps.users.serializers import UserSerializer
from .models import Library, LibraryBook

class LibraryBookSerializer(serializers.ModelSerializer):
    library_book_id = serializers.IntegerField(source='id', read_only=True)
    book = BookSerializer(many=False, read_only=True)

    class Meta:
        model = LibraryBook
        fields = ('library_book_id', 'is_completed', 'created_at', 'book',)
        read_only_fields = ('created_at',)

    def create(self, validated_data):
        library, _ = Library.objects.get_or_create(created_by=self.context['request'].user)
        book_data = self.context['request'].data.get('book_data')
        authors = book_data.pop('authors') if 'authors' in book_data.keys() else None
        if 'created_by' in book_data.keys() and book_data['created_by']:
            created_by = get_object_or_404(User.objects.filter(uid=book_data.pop('created_by')))
            book, created = Book.objects.get_or_create(created_by=created_by, **book_data)
            if created and authors:
                for author in authors:
                    author['name'] = author['name'].strip()
                    _ = Author.objects.create(book=book, **author)
            return LibraryBook.objects.create(library=library, book=book, **validated_data)
        else:
            book, created = Book.objects.get_or_create(**book_data)
            if created and authors:
                for author in authors:
                    author['name'] = author['name'].strip()
                    _ = Author.objects.create(book=book, **author)
            return LibraryBook.objects.create(library=library, book=book, **validated_data)

class LibrarySerializer(serializers.ModelSerializer):
    books = LibraryBookSerializer(many=True, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)
    book_count = serializers.SerializerMethodField(read_only=True)
    completed_count = serializers.SerializerMethodField(read_only=True)
    incomplete_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Library
        fields = (
            'id', 'created_by', 'created_at', 'book_count', 
            'completed_count', 'incomplete_count', 'books', 'uid',)
        read_only_fields = ('created_at',)
        extra_kwargs = {
            'uid': {'source': 'created_by', 'write_only': True}
        }

    def get_book_count(self, obj):
        return LibraryBook.objects.filter(library=obj.id).count()

    def get_completed_count(self, obj):
        return LibraryBook.objects.filter(
            library=obj.id, is_completed=True).count()
    
    def get_incomplete_count(self, obj):
        return LibraryBook.objects.filter(
            library=obj.id, is_completed=False).count()
