import socket
import requests
import traceback
import pdb
config={}
config['MANAGEMENT_HOST']="0.0.0.0"
config['MANAGEMENT_PORT']=5000

def get_nodes():
    r=requests.get("http://"+config['MANAGEMENT_HOST']+":"+str(config['MANAGEMENT_PORT'])+"/nodes/online")
    nodes=r.json()
    return nodes['nodes']

def partial(task_id):
    r = requests.get("http://"+config['MANAGEMENT_HOST']+":"+str(config['MANAGEMENT_PORT'])+'/partial/'+str(task_id))
    r = r.json()
    return r['res']

def fetch(task_id):
    r=requests.get("http://"+config['MANAGEMENT_HOST']+":"+str(config['MANAGEMENT_PORT'])+'/fetch/'+str(task_id))
    r=r.json()
    return r['stat']

def register_task(func):
    payload={"func": func}
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
            import pdb
            pdb.set_trace()
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
