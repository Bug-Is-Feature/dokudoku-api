import uuid

from rest_framework.test import APITestCase, APIRequestFactory

from apps.library.models import Library, LibraryBook
from apps.users.models import User
from ..models import Author, Book

class BooksAppTestSetUp(APITestCase):

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

        self.book_obj1 = Book.objects.create(
            title='test_book_1',
            subtitle='test_book_1_sub',
            category='test_book_1_category',
            thumbnail='test_book_1_thumbnail',
            description='test_book_1_desc',
            page_count=156,
            currency_code='THB',
            price=500,
            created_by=self.admin,
        )
        self.book_obj2 = Book.objects.create(
            title='test_book_2',
            subtitle='test_book_2_sub',
            category='test_book_2_category',
            thumbnail='test_book_2_thumbnail',
            description='test_book_2_desc',
            page_count=284,
            currency_code='THB',
            price=250,
            google_book_id='ed77c79706c3',
        )
        self.author_obj1 = Author.objects.create(
            book=self.book_obj1, name='test_book_1_author')
        self.author_obj2 = Author.objects.create(
            book=self.book_obj2, name='test_book_2_author_1')
        self.author_obj3 = Author.objects.create(
            book=self.book_obj2, name='test_book_2_author_2')
        
        self.library_obj1 = Library.objects.create(
            created_by=self.admin,
            is_changed=False
        )
        self.library_obj2 = Library.objects.create(
            created_by=self.user,
            is_changed=False
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
