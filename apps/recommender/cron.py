import datetime

from apps.library.models import Library
from apps.recommender.exceptions import FirebaseError, InsufficientBookError
from apps.recommender.recommender import BookRecommender

def recommender_scheduled_job():
    changed_library = Library.objects.filter(is_changed=True)
    changed_user = [library.created_by for library in changed_library]

    for user in changed_user:
        try:
            recommender = BookRecommender()
            recommender.create_recommend_result(user=user)

            library = Library.objects.get(created_by=user.uid)
            library.is_changed = False
            library.save()
            
            print(f'[{datetime.datetime.now()}] [CRON_KDTREE] [USER: {user.uid}] [STATUS] Completed')
        except FileNotFoundError:
            print(f'[{datetime.datetime.now()}] [CRON_KDTREE] [USER: {user.uid}] [STATUS] FileNotFoundError')
        except FirebaseError:
            print(f'[{datetime.datetime.now()}] [CRON_KDTREE] [USER: {user.uid}] [STATUS] FirebaseError')
        except InsufficientBookError:
            print(f'[{datetime.datetime.now()}] [CRON_KDTREE] [USER: {user.uid}] [STATUS] InsufficientBookError')

    print(f'{datetime.datetime.now()}  [CRON_KDTREE] COMPLETED')
