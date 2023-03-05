import uuid

from rest_framework.test import APITestCase, APIRequestFactory

from apps.books.models import Book
from apps.users.models import User
from ..models import Session

class SessionsAppTestSetUp(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin@admin.com'
        )
        self.user = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user@user.com',
        )
        self.book_obj = Book.objects.create(
            title='test_book',
            subtitle='test_book_sub',
            category='test_book_category',
            thumbnail='test_book_thumbnail',
            description='test_book_desc',
            page_count=284,
            currency_code='THB',
            price=250,
            google_book_id='ed77c79706c3',
        )
        self.session_obj = Session.objects.create(
            book=self.book_obj,
            duration=300,
            created_by=self.admin
        )
