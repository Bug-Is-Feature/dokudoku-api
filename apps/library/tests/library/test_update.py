from rest_framework import status
from rest_framework.test import force_authenticate

from ..test_setup import LibraryAppTestSetUp
from ...models import Library
from ...views import LibraryViewSet

class LibraryUpdateTest(LibraryAppTestSetUp):

    def test_library_update(self):
        '''
        Simulate an admin trying to edit a library data

        A response should return with edited library data
        '''
        request = self.factory.put(f'/api/library/{self.library_obj2.id}/', {
            "uid": self.user2.uid
        }, format='json')
        force_authenticate(request, user=self.admin)
        response = LibraryViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK,
            f'Expected http status 200, not {response.status_code}.')
        self.assertEqual(Library.objects.get(id=self.library_obj2.id).created_by.uid, self.user2.uid,
            f'Expected `{self.user2.uid}` as new library owner, but the object still belong to old owner.')

class LibraryUpdatePermissionTest(LibraryAppTestSetUp):

    def test_library_update_no_permission(self):
        '''
        Simulate a user trying to edit a library data
        which is not allowed

        An error message should return as response
        '''
        request = self.factory.put(f'/api/library/{self.library_obj2.id}/', {
            "uid": self.user2.uid
        }, format='json')
        force_authenticate(request, user=self.user1)
        response = LibraryViewSet.as_view({'put': 'partial_update'})(request, pk=self.library_obj2.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN,
            f'Expected http status 403, not {response.status_code}.')
        self.assertEqual(Library.objects.get(id=self.library_obj2.id).created_by.uid, self.user1.uid,
            f'Expected no change at library id:{self.library_obj2}, but the object got updated.')