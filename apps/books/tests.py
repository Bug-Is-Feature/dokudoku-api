import uuid

from django.core.exceptions import FieldError
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from apps.users.models import User
from .models import Author, Book
from .views import AuthorViewSet, BookViewSet

class TestSetUp(APITestCase):

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

class BookViewSetTest(TestSetUp):

    def test_book_viewset_admin(self):
        '''
        Simulate an admin trying to fetch all books in the system

        All books in the database should show up
        '''
        request = self.factory.get('/api/books/')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 2,
            f'Expected 2 books from admin view, not {len(response.data)}.')

    def test_book_viewset_user(self):
        '''
        Simulate a user trying to fetch all books they have in the system

        Every books that they own should show up (in this case is 0)
        '''
        request = self.factory.get('/api/books/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 0,
            f'Expected 0 book from user view, not {len(response.data)}.')

    def test_book_query_param_forbidden_action(self):
        '''
        Simulate a user trying to retrieve book data
        but passing both 2 query parameters (ggbookid, owner)
        which is not allowed

        An error message should show up
        '''
        request = self.factory.get('/api/books/', 
            {'ggbookid': 'ed77c79706c3', 'owner': self.admin.uid})
        force_authenticate(request, user=self.user)

        with self.assertRaises(FieldError):
            BookViewSet.as_view({'get': 'retrieve'})(request)

    def test_book_query_param_unknown(self):
        '''
        Simulate a user trying to retrieve book data
        but using unknown parameter in url

        An error message should show up
        '''
        request = self.factory.get('/api/books/', {'unknown_params': 'unknown_value'})
        force_authenticate(request, user=self.user)

        with self.assertRaises(FieldError):
            BookViewSet.as_view({'get': 'retrieve'})(request)

    def test_book_path_param(self):
        '''
        Simulate a user/admin trying to retrieve book data 
        by passing :id as path parameter

        A response should return with specific book data
        '''
        request = self.factory.get(f'/api/books/{self.book_obj1.id}/')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'get': 'retrieve'})(request, pk=self.book_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['title'], 'test_book_1',
            f'Expected `test_book_1` as title, not `{response.data["title"]}`.')

    def test_book_path_param_no_permission(self):
        '''
        Simulate a user trying to retrieve other user's book data 
        by passing :id of that book as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/books/{self.book_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'get': 'retrieve'})(request, pk=self.book_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')

    def test_book_create(self):
        '''
        Simulate a user trying to create a book

        A response should return with newly created book data
        and should be able to access user & authors data via response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_book_title",
            "subtitle": "test_book_subtitle",
            "category": "test_book_category",
            "thumbnail": "test_book_thumbnail",
            "description": "test_book_desc",
            "page_count": 134,
            "currency_code": "THB",
            "price": 100,
            "uid": self.user.uid,
            "authors": [
                {
                    "name": "test_book_author"
                }
            ]
        }, format='json')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
        self.assertEqual(response.data['title'], 'test_book_title',
            f'Expected `test_book_title` as book title, not `{response.data["title"]}`.')
        self.assertEqual(response.data['created_by']['uid'], self.user.uid,
            f'Expected `{self.user.uid}` as book owner, not `{response.data["created_by"]["uid"]}`.')
        self.assertEqual(response.data['authors'][0]['name'], 'test_book_author',
            f'Expected `test_book_author` as author name, not `{response.data["authors"][0]["name"]}`.')

    def test_book_create_error(self):
        '''
        Simulate a user trying to create a book
        but passing both 2 attributes (uid, google_book_id) 
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.post('/api/books/', {
            "title": "test_book_title",
            "subtitle": "test_book_subtitle",
            "category": "test_book_category",
            "thumbnail": "test_book_thumbnail",
            "description": "test_book_desc",
            "page_count": 134,
            "currency_code": "THB",
            "price": 100,
            "uid": self.user.uid,
            "google_book_id": "ed77c79706c3",
            "authors": [
                {
                    "name": "test_book_author"
                }
            ]
        }, format='json')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_book_update(self):
        '''
        Simulate a user/admin trying to edit a book

        A response should return with edited book data
        '''
        request = self.factory.put(f'/api/books/{self.book_obj1.id}/', {
            "subtitle": "edited_subtitle"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'put': 'partial_update'})(request, pk=self.book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK, 
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['subtitle'], 'edited_subtitle',
            f'Expected `edited_subtitle` as subtitle, not `{response.data["subtitle"]}`.')

    def test_book_update_no_permission(self):
        '''
        Simulate a user trying to edit a book
        but don't have a permission (not the owner of the book)
        
        An error message should return as response
        '''
        request = self.factory.put(f'/api/books/{self.book_obj1.id}/', {
            "subtitle": "edited_subtitle"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'put': 'partial_update'})(request, pk=self.book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')

    def test_book_delete(self):
        '''
        Simulate a user/admin trying to delete a book

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/books/{self.book_obj1.id}/')
        force_authenticate(request, user=self.admin)
        response = BookViewSet.as_view({'delete': 'destroy'})(request, pk=self.book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(Book.objects.filter(id=self.book_obj1.id).exists(),
            f'Expected no book with id `{self.book_obj1.id}` still exist.')

    def test_book_delete_no_permission(self):
        '''
        Simulate a user trying to delete a book 
        but don't have a permission (not the owner of the book)
        
        An error message should return as response
        '''
        request = self.factory.delete(f'/api/books/{self.book_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = BookViewSet.as_view({'delete': 'destroy'})(request, pk=self.book_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND,
            f'Expected http status 404, not {response.status_code}.')

class AuthorViewSetTest(TestSetUp):

    def test_author_viewset_admin(self):
        '''
        Simulate an admin trying to fetch all authors in the system

        All authors in the database should show up
        '''
        request = self.factory.get('/api/authors/')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertTrue(len(response.data) == 3,
            f'Expected 3 authors from admin view, not {len(response.data) == 3}.')
    
    def test_author_viewset_user(self):
        '''
        Simulate a user trying to fetch all authors in the system
        but fetching all authors is a privilege for admin

        An error message should return as response
        '''
        request = self.factory.get('/api/authors/')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'get': 'list'})(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_author_path_param(self):
        '''
        Simulate a user/admin trying to retrieve author data 
        by passing :id as path parameter

        A response should return with specific author data
        '''
        request = self.factory.get(f'/api/authors/{self.author_obj1.id}/')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'get': 'retrieve'})(request, pk=self.author_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data['name'], 'test_book_1_author',
            f'Expected `test_book_1_author` as name, not `{response.data["name"]}`.')

    def test_author_path_param_no_permission(self):
        '''
        Simulate a user trying to retrieve other user book's author 
        by passing :id of that author as path parameter
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.get(f'/api/authors/{self.author_obj1.id}/')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'get': 'retrieve'})(request, pk=self.author_obj1.id)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_author_create(self):
        '''
        Simulate a user/admin trying to create a book's author

        A response should return with newly created author data
        '''
        request = self.factory.post('/api/authors/', {
            "name": "test_create_author",
            "book_id": self.book_obj1.id
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'post': 'create'})(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
            f'Expected http status 201, not {response.status_code}.')
    
    def test_author_create_no_permission(self):
        '''
        Simulate a user/admin trying to create a book's author
        but don't have a permission (not the owner of the book)

        An error message should return as response
        '''
        request = self.factory.post('/api/authors/', {
            "name": "test_create_author",
            "book_id": self.book_obj2.id
        }, format='json')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'post': 'create'})(request)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_author_update(self):
        '''
        Simulate a user/admin trying to edit a book's author

        A response should return with edited author data
        '''
        request = self.factory.put(f'/api/authors/{self.author_obj1.id}/', {
            "name": "test_book_1_author_edited"
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'put': 'partial_update'})(request, pk=self.author_obj1.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
    
    def test_author_update_no_permission(self):
        '''
        Simulate a user/admin trying to edit a book's author
        but don't have a permission (not the owner of the book)

        An error message should return as response
        '''
        request = self.factory.put(f'/api/authors/{self.author_obj2.id}/', {
            "name": "test_book_2_author_1_edited"
        }, format='json')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'put': 'partial_update'})(request, pk=self.author_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')

    def test_author_delete(self):
        '''
        Simulate a user/admin trying to delete a book's author

        A response should return with 204 status
        '''
        request = self.factory.delete(f'/api/authors/{self.author_obj3.id}/')
        force_authenticate(request, user=self.admin)
        response = AuthorViewSet.as_view({'delete': 'destroy'})(request, pk=self.author_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT,
            f'Expected http status 204, not {response.status_code}.')
        self.assertFalse(Author.objects.filter(id=self.author_obj3.id).exists(),
            f'Expected no author with id `{self.author_obj3.id}` still exist.')

    def test_author_delete_no_permission(self):
        '''
        Simulate a user trying to delete a book 's author
        but don't have a permission (not the owner of the book)
        
        An error message should return as response
        '''
        request = self.factory.delete(f'/api/authors/{self.author_obj3.id}/')
        force_authenticate(request, user=self.user)
        response = AuthorViewSet.as_view({'delete': 'destroy'})(request, pk=self.author_obj3.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
