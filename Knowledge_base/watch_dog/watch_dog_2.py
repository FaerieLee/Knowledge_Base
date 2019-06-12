

import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler


def tick():
    try:
        if requests.get(url="http://localhost:9200", timeout=10).status_code != 200 or \
                requests.get(url="http://localhost:8000", timeout=10).status_code != 200:
            os.system("reboot")
    except:
        os.system("reboot")  


scheduler = BlockingScheduler()

scheduler.add_job(tick, 'interval', seconds=30)

scheduler.start()
