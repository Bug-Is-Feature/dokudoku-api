from rest_framework import viewsets

from .models import User, UserAchievement
from .serializers import UserSerializer, UserAchievementSerializer, UserAdminSerializer
from .permissions import UserPermission, UserAchievementPermission, UserAdminPermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

class UserAchievementViewSet(viewsets.ModelViewSet):
    queryset = UserAchievement.objects.all()
    serializer_class = UserAchievementSerializer
    permission_classes = (UserAchievementPermission,)

    def get_queryset(self):
        if self.request.user.is_admin:
            return UserAchievement.objects.all()
        else:
            return UserAchievement.objects.filter(user=self.request.user)
        
class UserAdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (UserAdminPermission,)

    def get_queryset(self):
        if self.action in ['list', 'retrieve', 'destroy']:
            return User.objects.filter(is_admin=True)
        else:
            return User.objects.all()