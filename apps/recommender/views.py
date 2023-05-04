from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from apps.books.models import Book
from .serializers import RecommenderSerializer
from .recommender import BookRecommender

class RecommenderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = RecommenderSerializer

    def list(self, request, *args, **kwargs):
        try:
            recommender = BookRecommender()
            result = recommender.get_recommend_result(uid=request.user)
            return Response(RecommenderSerializer(result, many=True).data, status=status.HTTP_200_OK)
        except FileNotFoundError:
            return Response(
                {'detail': 'Recommendation result not found, please try again later.'}, 
                status=status.HTTP_404_NOT_FOUND)
    