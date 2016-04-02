import socket
import subprocess
import psutil
import os
import requests
import soldier
import threading
from Queue import Queue

command=0
used_mem = psutil.virtual_memory()
mem = 100 - used_mem[2]

os.system("mpstat > cpuse.txt")

file = open("cpuse.txt","r")

count = 0

for line in file:
    count = count + 1
    if count==4:
        val=line.split()
        cpu_usage =  val[3]
cpu = float(cpu_usage)


payload = {"ip" : "112.32.172.12.12.11","mem" : mem , "cpu" : cpu}

r = requests.post("http://localhost:5000/register",payload)
k = r.json()
id = k['id']



def reportStat(q):
    try:
        while 1:
            if command== -1:
                print "Closing"
                return
            used_mem = psutil.virtual_memory()
            mem = 100 - used_mem[2]
            os.system("mpstat > cpuse.txt")
            file = open("cpuse.txt","r")
            count = 0
            for line in file:
                count = count + 1
                if count==4:
                    val=line.split()
            cpu_usage = val[3]
            cpu = float(cpu_usage)
            file.close()
            payload = {"cpu" : cpu ,"mem" : mem }
            r = requests.put("http://localhost:5000/stat/"+ str(id),payload)
    except Exception as e:
        q.put((repr(e), threading.current_thread.func_name))


def shutdown(s):
    global command
    command=-1
    payload = {"cpu" : cpu ,"mem" : mem , "status" : "Deleting"}
    r = requests.put("http://localhost:5000/stat/"+ str(id),payload)
    print r.text
    k = requests.delete("http://localhost:5000/stat/"+ str(id))
    print k.text
    s.close()


def recvfile(q):
    try:
        print "recvfile started"
        sock = socket.socket()
        sock.connect(('0.0.0.0', 1201))
        cloud_code = open("cloudcode.py","a")
        while 1:
            data = sock.recv(1)
            if data:
                print "data from test.py \t"+data
                if data=='$':
                    data=sock.recv(4)
                    if data=="exit":
                        cloud_code.close()
                    else:
                        cloud_code.write("$"+data)
                else:
                    cloud_code.write(data)
    except Exception as e:
        q.put((repr(e), threading.current_thread().getName()))
        return

def master_listener(q):
    try:
        s = socket.socket()
        s.connect(('0.0.0.0', 1200))
        s.send("node")
        print "Master Listener started"
        while 1:
            data = s.recv(1024)
            print data
            if data == '1':
                shutdown(s)
            if data == '2':
                restart()
            if data=='3':
                kill_all()
            if 'execute' in data:
                print "here"
                data= data.split(":")
                task = 1
                f_name = "agent" + str(task) + ".py"
                file = open(f_name,"w")
                file.write("import cloudcode")
                file.write("\n")
                file.write("cloudcode.ga('dsd')")
                file.close()
                print "here"
                os.system("python "+ f_name+"> xuz.txt")
                fprocess = soldier.run('python ' + f_name + ' > result.txt', background=True)

    except Exception as e:
        q.put((repr(e), threading.current_thread().getName()))
        return


def logger(q):
    print "Logger Thread started"
    try:
        while 1:
            data = q.get()
            print data
    except Exception as e:
        print repr(e)
        return


# Global queue where all threads leave there errors
q = Queue()

# threading.Thread(target=recvfile, args=(q,), name="File Receiver"),
threadlist = [threading.Thread(target=reportStat, args=(q,), name="Report Stat"),
            threading.Thread(target=master_listener, args=(q,), name="Master listener"),
            threading.Thread(target=logger, args=(q,), name="Logger")]


for t in threadlist:
    t.setDaemon(True)
    t.start()

while 1:
    pass


