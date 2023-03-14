from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.books.models import Book
from apps.books.models import User

# Create your models here.
class Session(models.Model):

    class TimerType(models.TextChoices):
        STOPWATCH = 'SW', _('Stopwatch')
        HOURGLASS = 'HG', _('Hourglass')

    book = models.ForeignKey(Book, related_name='sessions', on_delete=models.CASCADE, db_index=True)
    duration = models.PositiveIntegerField(null=False)
    timer_type = models.CharField(max_length=2, choices=TimerType.choices, null=False)
    created_by = models.ForeignKey(User, related_name='sessions', on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'session'
