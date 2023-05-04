import os
import uuid

from rest_framework.test import APITestCase, APIRequestFactory

from apps.books.models import Book
from apps.reading_sessions.models import Session
from apps.users.models import User
from apps.library.models import Library, LibraryBook

class RecommenderAppTestSetUp(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user1 = User.objects.create_user(
            uid='E701b7044323b44a89bb4174f829',
            email='user1@user.com',
        )
        self.user2 = User.objects.create_user(
            uid=uuid.uuid4().hex[:28],
            email='user2@user.com'
        )
        self.book_obj1 = Book.objects.create(
            id=1,
            title='test_book_1',
            page_count=156,
            currency_code='THB',
            price=500,
            created_by=self.user1,
        )
        self.book_obj2 = Book.objects.create(
            id=2,
            title='test_book_2',
            page_count=284,
            currency_code='THB',
            price=250,
            google_book_id='ed77c79706c3',
        )
        self.session = Session.objects.create(
            duration=600,
            timer_type='HG',
            book=self.book_obj1,
            created_by=self.user1,
        )
        self.library_obj = Library.objects.create(
            created_by=self.user1
        )
        self.library_book_obj1 = LibraryBook.objects.create(
            library=self.library_obj,
            book=self.book_obj1,
            is_completed=False,
        )
        self.library_book_obj2 = LibraryBook.objects.create(
            library=self.library_obj,
            book=self.book_obj2,
            is_completed=False,
        )

        self.path = './apps/recommender/tests/temp'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
