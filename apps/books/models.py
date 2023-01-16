from django.core.exceptions import ValidationError
from django.db import models

from apps.users.models import User

# Create your models here.        
class Book(models.Model):
    google_book_id = models.CharField(max_length=12, null=True, blank=True)
    title = models.CharField(max_length=255, null=False)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=40, null=True, blank=True)
    thumbnail = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    page_count = models.IntegerField(null=False)
    currency_code = models.CharField(max_length=3, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='books', on_delete=models.CASCADE, db_index=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.title

    def clean(self):
        if self.google_book_id is None and self.created_by is None:
            raise ValidationError({'VALIDATION_ERROR': 'google_book_id or created_by should exist in request body.'})
        if self.google_book_id and self.created_by:
            raise ValidationError({'VALIDATION_ERROR': 'Request body with google_book_id and created_by are not allowed, only one attribute can exist.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class Author(models.Model):
    book = models.ForeignKey(Book, related_name='authors', on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=55)

    class Meta:
        unique_together = ('book', 'name')
        db_table = 'book_author'

    def __str__(self):
        return self.name
