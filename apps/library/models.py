from django.db import models

from apps.books.models import Book
from apps.users.models import User

# Create your models here.  
class Library(models.Model):
    created_by = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_library'

    def __str__(self):
        return f'{self.created_by}'

class LibraryBook(models.Model):
    library = models.ForeignKey(Library, related_name='books', on_delete=models.CASCADE, db_index=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_index=True)
    is_completed = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('library', 'book',)
        db_table = 'library_book'
        
    def __str__(self):
        return f'{self.library}: {self.book}'