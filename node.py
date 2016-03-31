import socket
import subprocess
import psutil
import os
import requests
import thread



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
    payload = {"cpu" : cpu ,"mem" : mem , "status" : "Deleting"}
    r = requests.put("http://localhost:5000/stat/"+ str(id),payload)
    print r.text
    k = requests.delete("http://localhost:5000/stat/"+ str(id))
    print k.text
    s.close()




def ulpoad_data(data):
    while 1:
        file = open("agent.py","w")
        file.write(data)
        file.close
        break


thread.start_new_thread(reportStat,())

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
    if 'upload' in data:
        thread.start_new_thread(upload_data,(data))
    if 'exec' in data:
        #create new file agent.py
        #exec printcval(a,b,c)
        os.system("pyhton agent.py")

