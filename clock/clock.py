from flask import Flask
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
app = Flask(__name__)

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')



if __name__ == '__main__':
	app.run()
	sched.start()

