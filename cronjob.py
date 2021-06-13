from apscheduler.schedulers.blocking import BlockingScheduler
from scheduler import cronjob

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BlockingScheduler(job_defaults=job_defaults)
scheduler.add_job(cronjob, "interval", seconds=600)

scheduler.start()