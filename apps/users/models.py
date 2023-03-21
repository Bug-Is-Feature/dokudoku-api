from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

from apps.achievements.models import Achievement

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, uid, email):
        if not uid:
            raise ValueError('User must have an UID')
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            uid=uid,
            email=self.normalize_email(email),
        )
        user.set_unusable_password()
        user.save(using=self._db)

        return user

    def create_superuser(self, uid, email):
        user = self.create_user(uid, email)
        user.is_admin = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    uid = models.CharField(max_length=28, primary_key=True, unique=True, null=False)
    email = models.CharField(max_length=255, null=False)
    current_lvl = models.PositiveIntegerField(default=1)
    current_exp = models.PositiveIntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'uid'

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.uid
    
class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, db_index=True)

    class Meta:
        unique_together = ('user', 'achievement',)
        db_table = 'user_achievement'

    def __str__(self):
        return f'{self.user.uid}: {self.achievement.id}'
