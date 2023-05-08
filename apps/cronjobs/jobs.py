import datetime
import logging

from apps.library.models import Library
from apps.recommender.exceptions import FirebaseError, InsufficientBookError
from apps.recommender.recommender import BookRecommender

def recommender_scheduled_job():
    start_time = datetime.datetime.now()
    logger = logging.getLogger(__name__)
    logger.info(f'Running `recommender_scheduled_job` jobs')
    changed_library = Library.objects.filter(is_changed=True)
    changed_user = [library.created_by for library in changed_library]

    success = 0
    for user in changed_user:
        try:
            recommender = BookRecommender()
            recommender.create_recommend_result(user=user)

            library = Library.objects.get(created_by=user.uid)
            library.is_changed = False
            library.save()
            
            success += 1
            logger.info(f'user: {user.uid}, status: completed')
        except FileNotFoundError:
            logger.error(f'user: {user.uid}, status: FileNotFoundError')
        except FirebaseError:
            logger.error(f'user: {user.uid}, status: FirebaseError')
        except InsufficientBookError:
            logger.error(f'user: {user.uid}, status: InsufficientBookError')

    logger.info(f'Job finished, success: {success}, fail: {len(changed_user) - success}, runtime {str(datetime.datetime.now() - start_time)}')
