from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from iso4217 import Currency
from rest_framework import serializers

from apps.library.models import Library
from apps.users.serializers import UserSerializer
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name',)
    
    def create(self, validated_data):
        book_id = self.context['request'].data.get('book_id')
        book = get_object_or_404(Book.objects.filter(id=book_id))
        user = self.context['request'].user
        if book.google_book_id:
            if user.is_admin:
                return Author.objects.create(book=book, **validated_data)
            else:
                raise PermissionDenied
        elif book.created_by == user or user.is_admin:
            response = Author.objects.create(book=book, **validated_data)
            library = Library.objects.get(created_by=self.context['request'].user)
            if not library.is_changed:
                library.is_changed = True
                library.save()
            return response
        else:
            raise PermissionDenied
    
    def update(self, instance, validated_data):
        response = super().update(instance, validated_data)
        library = Library.objects.get(created_by=self.context['request'].user)
        if not library.is_changed:
            library.is_changed = True
            library.save()
        return response

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'title', 'subtitle', 'category', 
            'thumbnail', 'description', 'page_count', 
            'currency_code', 'price', 'created_by', 
            'google_book_id', 'uid', 'authors', 'created_at')
        read_only_fields = ('created_at',)
        extra_kwargs = {
            'uid': {'source': 'created_by', 'write_only': True},
        }
    
    def create(self, validated_data):
        authors = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        for author in authors:
            Author.objects.create(book=book, **author)
        return book

    def validate(self, attrs):
        if 'currency_code' in attrs.keys() and attrs['currency_code'] and not attrs['currency_code'].lower() in Currency.__members__.keys():
            raise serializers.ValidationError({'currency_code': 'Invalid currency code.'})
        if 'price' in attrs.keys() and attrs['price'] < 0:
            raise serializers.ValidationError({'price': 'Ensure this field is greater than zero.'})
        if 'google_book_id' in attrs.keys() and len(attrs['google_book_id']) != 12:
            raise serializers.ValidationError({'google_book_id': 'Ensure this field has length of 12 characters.'})

        return super().validate(attrs)
    
    def save(self, **kwargs):
        library = Library.objects.get(created_by=self.context['request'].user)
        if not library.is_changed:
            library.is_changed = True
            library.save()
        return super().save(**kwargs)
