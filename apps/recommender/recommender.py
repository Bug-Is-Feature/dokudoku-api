import pickle
import pandas as pd
import re

from django.conf import settings
from django.db.models import Max, Sum
from firebase_admin import storage
from operator import itemgetter
from sklearn.neighbors import KDTree

from apps.books.models import Author, Book
from apps.library.models import Library, LibraryBook
from apps.reading_sessions.models import Session
from .exceptions import FirebaseError, InsufficientBookError

if not settings.TESTING:
    bucket = storage.bucket()

class BookRecommender():

    def __init__(self):
        self.PICKLE_PATH = './apps/recommender/pickle'
        if settings.DEBUG:
            self.bucket_path = 'user_book_recommendation/mock/'
        else:
            self.bucket_path = 'user_book_recommendation/'

    def book_to_text(self, book):
        authors = Author.objects.filter(book=book)
        authors = ', '.join([author.name for author in authors])
        return str(
            (book.title if book.title else '') + ' ' + 
            (book.subtitle if book.subtitle else '') + ' ' + 
            authors + ' ' + 
            (book.description if book.description else '') + ' ' + 
            (book.category if book.category else '')).strip().lower()

    def create_recommend_result(self, user, k=4):
        bow_vector = pickle.load(open(self.PICKLE_PATH + '/bow_vector.pickle', 'rb'))

        # build tree
        library, _ = Library.objects.get_or_create(created_by=user)
        library_books = LibraryBook.objects.filter(library=library, is_completed=False).order_by('pk')
        if not library_books:
            raise InsufficientBookError('User have no incomplete book in library.')
        elif len(library_books) == 1:
            raise InsufficientBookError('User only have one incomplete book in library.')

        text = []
        data_pk = [library_book.book.id for library_book in library_books]
        for library_book in library_books:
            text.append(self.book_to_text(library_book.book))

        data_bow = bow_vector.transform(text).toarray()
        tree = KDTree(data_bow)

        # create target
        recommender = BookRecommender()
        subquery = (Session.objects.filter(created_by=user)
                                .values('book_id')
                                .order_by('book_id')
                                .annotate(total_duration=Sum('duration')))
        if subquery:
            most_read_book_id = subquery.filter(total_duration=
                list(subquery.aggregate(Max('total_duration')).values())[0]).first().get('book_id')
            target = Book.objects.get(id=most_read_book_id)
        else:
            target = Book.objects.get(id=data_pk[0])
        target_bow = bow_vector.transform(pd.Series(recommender.book_to_text(target))).toarray()

        # get result
        if len(tree.data) < 4:
            k = len(tree.data)

        _, index = tree.query(target_bow, k=k)

        recommend_index = [idx for idx in index[0] if itemgetter(idx)(data_pk) != target.id]
        result_text = ','.join(re.sub(r'[()]', '', str(itemgetter(*recommend_index)(data_pk))).split(', '))

        if not settings.TESTING:
            try:
                blob = bucket.blob(self.bucket_path + f'{user.uid}.txt')
                blob.upload_from_string(result_text)
            except:
                raise FirebaseError
        else:
            with open(f'./apps/recommender/tests/temp/{user.uid}.txt', 'w') as f:
                f.write(result_text)

    def get_recommend_result(self, uid):
        if not settings.TESTING:
            blob = bucket.blob(self.bucket_path + f'{uid}.txt')
            if not blob.exists():
                raise FileNotFoundError('Recommendation file is not found on firebase.')
            return Book.objects.filter(pk__in=[int(idx) for idx in blob.download_as_text().split(',')])
        else:
            with open(f'./apps/recommender/tests/temp/{uid}.txt', 'r') as f:
                return Book.objects.filter(pk__in=[int(idx) for idx in f.read().split(',')])
