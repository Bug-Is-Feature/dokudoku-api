from django.db import models

from apps.books.models import Book
from apps.books.models import User

# Create your models here.
class Session(models.Model):
    book = models.ForeignKey(Book, related_name='sessions', on_delete=models.CASCADE, db_index=True)
    duration = models.IntegerField(null=False)
    created_by = models.ForeignKey(User, related_name='sessions', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'session'
