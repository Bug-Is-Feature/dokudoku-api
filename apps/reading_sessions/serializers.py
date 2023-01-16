from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from apps.books.models import Book
from apps.books.serializers import BookSerializer
from apps.users.serializers import UserSerializer
from .models import Session

class SessionSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=False, read_only=True)
    created_by = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Session
        fields = (
            'id', 'book', 'duration', 'created_by',
            'book_id', 'uid', 'created_at')
        read_only_fields = ('created_at',)
        extra_kwargs = {
            'book_id': {'source': 'book', 'write_only': True},
            'uid': {'source': 'created_by', 'write_only': True},
        }
    
    def create(self, validated_data):
        book_id = self.context['request'].data.get('book_id')
        book = get_object_or_404(Book.objects.filter(id=book_id))
        user = self.context['request'].user
        if book.created_by == user or book.google_book_id or user.is_admin:
            return super().create(validated_data)
        else:
            raise PermissionDenied
