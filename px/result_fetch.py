from Queue import Queue
from . import config
import requests
def result_loop(task_id):
    q= Queue()
    while 1:
        r = requests.get("http://"+config['MANAGEMENT_HOST']+":"+str(config['MANAGEMENT_PORT'])+"/results/"+str(task_id))
        r=r.json()
        for result in r:
            q.put(result)