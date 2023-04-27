from django.urls import path, include
from rest_framework import routers
from .views import RecommenderViewSet

router = routers.DefaultRouter()
router.register('recommendation', RecommenderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]