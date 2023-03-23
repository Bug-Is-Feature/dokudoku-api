from django.urls import path, include
from rest_framework import routers
from .views import AchievementViewSet, AchievementGroupViewSet

router = routers.DefaultRouter()
router.register('achievements', AchievementViewSet)
router.register('achievement-groups', AchievementGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]