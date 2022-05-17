import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from eld_admin.models import Log, Driver


class LogCreator:

    @staticmethod
    def create_logs():
        for driver in Driver.objects.all():
            date = datetime.datetime.now().date().isoformat()
            Log(date=date, driver=driver).save()

    def __init__(self):
        self.scheduler = BackgroundScheduler()

        self.scheduler.add_job(LogCreator.create_logs, 'interval', hours=24)

    def start(self):
        self.scheduler.start()
