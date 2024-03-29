from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class AchievementGroup(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)

    class Meta:
        db_table = 'achievement_group'

    def __str__(self):
        return self.name

class Achievement(models.Model):

    class UnlockCondition(models.TextChoices):
        BOOK_AMOUNT = 'BK_A', _('Book Amount')
        INCOMPLETE_BOOK_AMOUNT = 'IB_A', _('Incomplete Book Amount')
        TOTAL_READING_HOUR = 'T_RH', _('Total Reading Hours')
        STOPWATCH_READING_HOUR = 'S_RH', _('Stopwatch Reading Hours')
        HOURGLASS_READING_HOUR = 'H_RH', _('Hourglass Reading Hours')

    name = models.CharField(max_length=50, unique=True, null=False)
    description = models.TextField(null=True, blank=True)
    group = models.ForeignKey(AchievementGroup, on_delete=models.SET_NULL, null=True, db_index=True)
    locked_thumbnail = models.TextField()
    unlocked_thumbnail = models.TextField()
    condition = models.CharField(max_length=4, choices=UnlockCondition.choices, null=False)
    threshold = models.PositiveIntegerField(null=False)
    available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'achievement'

    def __str__(self):
        return self.name