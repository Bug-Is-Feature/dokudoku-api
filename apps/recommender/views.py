from django.db.models import Max, Sum
from django.shortcuts import get_list_or_404, get_object_or_404
from operator import itemgetter
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from apps.books.models import Author, Book
from apps.library.models import Library, LibraryBook
from apps.reading_sessions.models import Session
from .serializers import RecommenderSerializer
from .recommender import BookRecommender

class RecommenderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LibraryBook.objects.all()
    serializer_class = RecommenderSerializer

    def book_to_text(self, book):
        authors = Author.objects.filter(book=book)
        authors = ', '.join([author.name for author in authors])
        return str(
            (book.title if book.title else '') + ' ' + 
            (book.subtitle if book.subtitle else '') + ' ' + 
            authors + ' ' + 
            (book.description if book.description else '') + ' ' + 
            (book.category if book.category else '')).strip().lower()

    def list(self, request, *args, **kwargs):
        library, _ = Library.objects.get_or_create(created_by=self.request.user)
        library_books = get_list_or_404(
            LibraryBook.objects.filter(library=library, is_completed=False))

        subquery = (Session.objects.filter(created_by=request.user)
                                   .values('book_id')
                                   .order_by('book_id')
                                   .annotate(total_duration=Sum('duration')))
        if subquery:
            most_read_book_id = subquery.filter(total_duration=
                list(subquery.aggregate(Max('total_duration')).values())[0]).first().get('book_id')
            target = self.book_to_text(Book.objects.get(id=most_read_book_id))

            data_pk = []
            text = []
            for library_book in library_books:
                book = library_book.book
                if book.id != most_read_book_id:
                    data_pk.append(book.id)
                    text.append(self.book_to_text(book))

            recommend_index = list(BookRecommender.k_neighbors(self, data=text, target=target))
            if len(recommend_index) == 1:
                return Response(
                    RecommenderSerializer(Book.objects.filter(pk=itemgetter(*recommend_index)(data_pk)), many=True).data, 
                    status=status.HTTP_200_OK)
            else:
                return Response(
                    RecommenderSerializer(Book.objects.filter(pk__in=itemgetter(*recommend_index)(data_pk)), many=True).data, 
                    status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'user session not found.'}, status=status.HTTP_404_NOT_FOUND)