from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import viewsets

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .permissions import AuthorPermission, BookPermission

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (BookPermission,)

    def get_queryset(self):
        # if query parameter exist
        if self.request.GET:
            params = self.request.GET.copy()
            google_book_id = params.pop('ggbookid').pop() if 'ggbookid' in params.keys() else None
            owner = params.pop('owner').pop() if 'owner' in params.keys() else None

            if params:
                raise FieldError({'QUERY_PARAM_ERROR': f'Unknown query parameter: {list(params.keys())}'})
            elif google_book_id and owner:
                raise FieldError({'QUERY_PARAM_ERROR': 'Passing both ggbookid and owner at the same time are forbidden'})
            elif google_book_id:
                return get_object_or_404(Book.objects.filter(google_book_id=google_book_id))
            elif owner:
                return get_list_or_404(Book.objects.filter(created_by=owner))
            else:
                raise FieldError({'QUERY_PARAM_ERROR': 'Unknown error'})
        else:
            if self.request.user.is_admin:
                return Book.objects.all()
            else:
                return Book.objects.filter(created_by=self.request.user)

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (AuthorPermission,)
