from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserAchievementViewSet, UserAdminViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('user-admin', UserAdminViewSet)
router.register('user-achievements', UserAchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]