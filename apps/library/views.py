from django.core.exceptions import FieldError
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from apps.books.models import Book
from .models import Library, LibraryBook
from .permissions import LibraryPermission, LibraryBookPermission
from .serializers import LibrarySerializer, LibraryBookSerializer

# Create your views here.
class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = (LibraryPermission,)

    def get_queryset(self):
        # if query parameter exist
        if self.request.GET:
            params = self.request.GET.copy()
            uid = params.pop('uid').pop() if 'uid' in params.keys() else None

            if params:
                raise FieldError({'QUERY_PARAM_ERROR': f'Unknown query parameter: {list(params.keys())}'})
            elif uid:
                return get_object_or_404(Library.objects.filter(created_by=uid))
            else:
                raise FieldError({'QUERY_PARAM_ERROR': 'Unknown error'})
        else:
            if self.request.user.is_admin:
                return Library.objects.all()
            else:
                if not Library.objects.filter(created_by=self.request.user).exists():
                    Library.objects.create(created_by=self.request.user)
                return Library.objects.filter(created_by=self.request.user)

class LibraryBookViewSet(viewsets.ModelViewSet):
    queryset = LibraryBook.objects.all()
    serializer_class = LibraryBookSerializer
    permission_classes = (LibraryBookPermission,)

    def get_queryset(self):
        # if query parameter exist
        if self.request.GET:
            params = self.request.GET.copy()
            book_id = params.pop('book_id').pop() if 'book_id' in params.keys() else None
            library_id = params.pop('library_id').pop() if 'library_id' in params.keys() else None

            if params:
                raise FieldError({'QUERY_PARAM_ERROR': f'Unknown query parameter: {list(params.keys())}'})
            elif book_id and library_id:
                return get_object_or_404(LibraryBook.objects.filter(library=library_id, book=book_id))
            elif library_id:
                return get_list_or_404(LibraryBook.objects.filter(library=library_id))
            elif book_id:
                if self.request.user.is_admin:
                    return get_list_or_404(LibraryBook.objects.filter(book=book_id))
                else:
                    library = get_object_or_404(Library.objects.filter(created_by=self.request.user))
                    return get_object_or_404(LibraryBook.objects.filter(library=library, book=book_id))
            else:
                raise FieldError({'QUERY_PARAM_ERROR': 'Unknown error'})
        else:
            if self.request.user.is_admin:
                return LibraryBook.objects.all()
            else:
                library = get_object_or_404(Library.objects.filter(created_by=self.request.user))
                return LibraryBook.objects.filter(library=library)

    def destroy(self, request, *args, **kwargs):
        library = Library.objects.get(created_by=request.user)
        library_book = self.get_object()
        book = get_object_or_404(Book.objects.filter(id=library_book.book.id))
        if book.created_by and book.created_by == request.user:
            # delete book will cascade library_book, if not use _ then the delete() is not trigger
            _ = Book.objects.filter(id=book.id).delete()
            if not library.is_changed:
                library.is_changed = True
                library.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        response = super().destroy(request, *args, **kwargs)
        if not library.is_changed:
            library.is_changed = True
            library.save()
        return response
        