import socket
import requests
import traceback
# from . import result_fetch
import threading
import pdb
config={}
config['MANAGEMENT_HOST']="0.0.0.0"
config['MANAGEMENT_PORT']=5000
client_id=0


def init():
    r = requests.post("http://"+config['MANAGEMENT_HOST']+":"+str(config['MANAGEMENT_PORT'])+"/clientreg")
    r = r.json()
    if 'success' in r['msg']:
        global client_id
        client_id = r['id']

def get_nodes():
    r=requests.get("http://"+config['MANAGEMENT_HOST']+":"+str(config['MANAGEMENT_PORT'])+"/nodes/online")
    nodes=r.json()
    return nodes['nodes']

def partial(task_id):
    r = requests.get("http://"+config['MANAGEMENT_HOST']+":"+str(config['MANAGEMENT_PORT'])+'/partial/'+str(task_id))
    r = r.json()
    return r['res']

def fetch(task_id):
    r=requests.get("http://"+config['MANAGEMENT_HOST']+":"+str(config['MANAGEMENT_PORT'])+'/fetch/'+str(client_id)+"/"+str(task_id))
    r=r.json()
    return r

def register_task(func):
    payload={"func": func,"client_id": client_id}
    print "http://" + config['MANAGEMENT_HOST'] + ":" + str(config['MANAGEMENT_PORT']) + '/taskreg'
    r = requests.post(
        "http://" + config['MANAGEMENT_HOST'] + ":" + str(config['MANAGEMENT_PORT']) + '/taskreg',payload)
    r = r.json()
    return r['id']

def execute(function,args,max_nodes=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect(("0.0.0.0",1200))
        try:
            task_id=register_task("execute:" + function+'('+'"'+args+'"'+")")
            s.send("user")
            s.send("execute:" +str(task_id)+":"+function+'('+'"'+args+'"'+")")
        except Exception as e:
            print str(e)
            return -1
        finally:
            s.close()
        return task_id
    except Exception as e:
        print traceback.format_exc()
        print str(e)
        return -1


def deploy(filename):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        nodes= get_nodes()
        # pdb.set_trace()
        for node in nodes:
            print node
            ip, port= node['ip'].split(":")
            s.connect((ip, 1201))
            f = open(filename, "rb")
            try:
                for line in f:
                    s.send(line)
                s.close()
            except Exception as e:
                raise e
    except Exception as e:
        print str(e)
        return -1

__author__ = 'gaurav'
