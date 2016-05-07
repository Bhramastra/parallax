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

def execute(function,args,max_nodes=10):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect(("0.0.0.0",1200))
        try:
            s.send("user")
            s.send("execute:" + function+'('+args+")")

        except Exception as e:
            print traceback.format_exc()
            print str(e)
            return -1
        finally:
            s.close()
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
                    print line
                    s.send(line)
                s.close()
            except Exception as e:
                raise e
    except Exception as e:
        print str(e)
        return -1

__author__ = 'gaurav'
