from django.urls import path, include
from rest_framework import routers
from .views import LibraryViewSet, LibraryBookViewSet

router = routers.DefaultRouter()
router.register('library', LibraryViewSet)
router.register('library-books', LibraryBookViewSet)

urlpatterns = [
    path('', include(router.urls)),
]