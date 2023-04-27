from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...models import Library
from ...serializers import LibrarySerializer
from ...views import LibraryViewSet

class LibraryListTest(LibraryAppTestSetUp):

    def test_library_list_admin_view(self):
        '''
        Simulate an admin trying to fetch all library in the system

        All library in the database should show up
        '''
        request = self.factory.get('/api/library/')
        force_authenticate(request, self.admin)
        response = LibraryViewSet.as_view({'get': 'list'})(request)

        library = Library.objects.all()
        serializers = LibrarySerializer(library, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get all library in the database, but the response is not right.')
        self.assertTrue(len(response.data) == 2,
            f'Expected 2 library from admin view, not {len(response.data)}.')

    def test_library_list_user_view(self):
        '''
        Simulate a user trying to fetch their library in the system

        One library which is their own should show up
        '''
        request = self.factory.get('/api/library/')
        force_authenticate(request, user=self.user1)
        response = LibraryViewSet.as_view({'get': 'list'})(request)

        library = Library.objects.filter(created_by=self.user1.uid)
        serializers = LibrarySerializer(library, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get user\'s library data, but the response is not right.')
        self.assertTrue(len(response.data) == 1,
            f'Expected only one library from user view, not {len(response.data)}.')
        
    def test_library_list_auto_create(self):
        '''
        Simulate a user trying to fetch their library in the system
        but the library is not exist

        System will automatically create library and their library should return as response
        '''
        request = self.factory.get('/api/library/')
        force_authenticate(request, user=self.user2)
        response = LibraryViewSet.as_view({'get': 'list'})(request)

        library = Library.objects.filter(created_by=self.user2.uid)
        serializers = LibrarySerializer(library, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(response.data, serializers.data,
            'Expected to get user\'s library data, but the response is not right.')
        self.assertTrue(len(response.data) == 1,
            f'Expected only one library from user view, not {len(response.data)}.')
