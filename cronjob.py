from apscheduler.schedulers.blocking import BlockingScheduler
from scheduler import cronjob

scheduler = BlockingScheduler()
scheduler.add_job(cronjob, "interval", seconds=30)

scheduler.start()