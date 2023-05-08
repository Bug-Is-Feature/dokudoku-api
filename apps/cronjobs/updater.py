from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import recommender_scheduled_job

def start():
    scheduler = BackgroundScheduler({'apscheduler.timezone': 'Asia/Bangkok'})
    scheduler.add_job(recommender_scheduled_job, 'cron', hour='0,12')
    scheduler.start()
