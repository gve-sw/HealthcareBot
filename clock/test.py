from flask import Flask
from flask_apscheduler import APScheduler
import datetime


class Config(object):
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()
app = Flask(__name__)
SEC_INTERVAL=5

# interval examples
@scheduler.task('interval', id='do_job_1', seconds=SEC_INTERVAL, misfire_grace_time=900)
def job1():
    print('Job 1 executed')
    print(datetime.datetime.now())



@scheduler.task('cron', id='do_job_3', day_of_week='mon-fri', hour=16 , minute=48)
def job3():
    print('Job 3 executed')

@app.route('/update',methods=['GET'])
def update():
     scheduler.remove_job(id='do_job_1')
     scheduler.add_job('interval', id='do_job_1', seconds=SEC_INTERVAL, misfire_grace_time=900)

     return 'ok',200

if __name__ == '__main__':
    
    app.config.from_object(Config())

    # it is also possible to enable the API directly
    # scheduler.api_enabled = True
    scheduler.init_app(app)
    scheduler.start()

    app.run()