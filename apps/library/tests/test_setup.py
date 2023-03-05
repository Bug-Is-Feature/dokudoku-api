import uuid

from rest_framework.test import APITestCase, APIRequestFactory

from apps.books.models import Book
from apps.users.models import User
from ..models import Library, LibraryBook

class LibraryAppTestSetUp(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin = User.objects.create_superuser(
            uid=uuid.uuid4().hex[:28],
            email='admin@admin.com'
        )
        self.user1 = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user1@user.com',
        )
        self.user2 = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user2@user.com'
        )
        self.book_obj1 = Book.objects.create(
            title='test_book_1',
            page_count=156,
            currency_code='THB',
            price=500,
            created_by=self.admin,
        )
        self.book_obj2 = Book.objects.create(
            title='test_book_2',
            page_count=284,
            currency_code='THB',
            price=250,
            google_book_id='ed77c79706c3',
        )
        self.library_obj1 = Library.objects.create(
            created_by=self.admin
        )
        self.library_obj2 = Library.objects.create(
            created_by=self.user1
        )
        self.library_book_obj1 = LibraryBook.objects.create(
            library=self.library_obj1,
            book=self.book_obj1,
            is_completed=False,
        )
        self.library_book_obj2 = LibraryBook.objects.create(
            library=self.library_obj2,
            book=self.book_obj2,
            is_completed=False,
        )