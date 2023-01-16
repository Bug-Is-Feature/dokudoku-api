from rest_framework import viewsets

from .models import User
from .serializers import UserSerializer
from .permissions import UserPermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)
    # lookup_field = 'email'
    # lookup_value_regex = "[^/]+"