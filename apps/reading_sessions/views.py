from django.core.exceptions import FieldError
from django.shortcuts import get_list_or_404
from rest_framework import viewsets

from .models import Session
from .serializers import SessionSerializer
from .permissions import SessionPermission

# Create your views here.
class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = (SessionPermission,)

    def get_queryset(self):
        # if query parameter exist
        if self.request.GET:
            params = self.request.GET.copy()
            book_id = params.pop('bookid').pop() if 'bookid' in params.keys() else None
            owner = params.pop('owner').pop() if 'owner' in params.keys() else None

            if params:
                raise FieldError({'QUERY_PARAM_ERROR': f'Unknown query parameter: {list(params.keys())}'})
            elif book_id and owner:
                return get_list_or_404(Session.objects.filter(book=book_id, created_by=owner))
            elif book_id:
                if self.request.user.is_admin:
                    return get_list_or_404(Session.objects.filter(book=book_id))
                else:
                    return get_list_or_404(Session.objects.filter(book=book_id, created_by=self.request.user))
            elif owner:
                return get_list_or_404(Session.objects.filter(created_by=owner))
            else:
                raise FieldError({'QUERY_PARAM_ERROR': 'Unknown error'})
        else:
            if self.request.user.is_admin:
                return Session.objects.all()
            else:
                return Session.objects.filter(created_by=self.request.user)