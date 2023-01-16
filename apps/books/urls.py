from django.urls import path, include
from rest_framework import routers
from .views import AuthorViewSet, BookViewSet

router = routers.DefaultRouter()
router.register('books', BookViewSet)
router.register('authors', AuthorViewSet)

urlpatterns = [
    path('', include(router.urls)),
]