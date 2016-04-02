import socket
import subprocess
import psutil
import os
import requests
import thread


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



def reportStat():
    while 1:
        if command== -1:
            print "Closing"
            thread.exit()
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
        file.close()
        payload = {"cpu" : cpu ,"mem" : mem }
        r = requests.put("http://localhost:5000/stat/"+ str(id),payload)


def shutdown(s):
    global command
    command=-1
    payload = {"cpu" : cpu ,"mem" : mem , "status" : "Deleting"}
    r = requests.put("http://localhost:5000/stat/"+ str(id),payload)
    print r.text
    k = requests.delete("http://localhost:5000/stat/"+ str(id))
    print k.text
    s.close()


def recvfile():
    print "recvfile started"
    sock = socket.socket()
    sock.connect(('0.0.0.0', 1201))
    cloud_code = open("cloudcode.py","w")
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


thread.start_new_thread(reportStat,())
thread.start_new_thread(recvfile,())
s=socket.socket()
s.connect(('0.0.0.0',1200))
while 1:
    data=s.recv(1024)
    print data
    if data=='1':
        shutdown(s)
    if data=='2':
        restart()
    if data=='3':
        kill_all()
    if 'exec' in data:
        #create new file agent.py
        #exec printcval(a,b,c)
        os.system("pyhton agent.py")

