from django.urls import path, include
from rest_framework import routers
from .views import AchievementViewSet

router = routers.DefaultRouter()
router.register('achievements', AchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]