# -*-coding:utf-8-*-

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import hashlib
import os


val_str = '{"data": [{"year": 2006, "publisher": "Elsevier Science Inc.", ' \
          '"id": "4cb78d36-d559-4010-83b9-a76fdbb5cf64", ' \
          '"title": "Random subspace method for multivariate feature selection", "n_citation": 129, ' \
          '"sub_abstract": "In a growing number of domains data captured encapsulates as many features ' \
          'as possible. This poses a challenge to classical pattern recognition techni", ' \
          '"authors": [{"name": "Carmen Lai"}, {"name": "Marcel J. T. Reinders"}, ' \
          '{"name": "Lodewyk F. A. Wessels"}], "doi": "10.1016/j.patrec.2005.12.018"}], ' \
          '"page_num": 1, "result_num": 1}'

m2 = hashlib.md5()
m2.update(val_str.encode('utf-8'))
val_hash = m2.hexdigest()

paras_dict = {"search_content": "Random subspace method for multivariate feature selection"}


def tick():

    try:
        result = requests.post(url="http://localhost:8000/paper/search_general", timeout=15, data=paras_dict).text
        if isinstance(result, str):
            m3 = hashlib.md5()
            m3.update(result.encode('utf-8'))
            result_hash = m3.hexdigest()
            if result_hash == val_hash:
                pass
            else:
                os.system("reboot")
        else:
            os.system("reboot")
    except:
        os.system("reboot")


scheduler = BlockingScheduler()

scheduler.add_job(tick, 'interval', seconds=60)

scheduler.start()
