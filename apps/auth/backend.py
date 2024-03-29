from rest_framework import authentication
from firebase_admin import auth
from .exceptions import NoAuthToken, InvalidAuthToken, FirebaseError

from apps.users.models import User

class FirebaseBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        # get request header
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            raise NoAuthToken('No auth token provided')

        # get ID token from request header
        id_token = auth_header.split(' ').pop()
        if not id_token:
            raise NoAuthToken('No auth token provided')

        decoded_token = None
        # check if token valid
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken('Invalid auth token')

        if not id_token or not decoded_token:
            return None

        # get unique user ID
        try:
            uid = decoded_token.get('uid')
        except Exception:
            raise FirebaseError()

        user, created = User.objects.get_or_create(uid=uid)

        return (user, None)
