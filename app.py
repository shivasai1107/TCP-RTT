#!flask/bin/python

from __future__ import print_function
from flask import Flask, render_template, request, redirect
from flask import send_file
import os
import sys
import socket
import threading
import time
from multiprocessing import Process
import subprocess
#from influxdb import InfluxDBClient

app = Flask(__name__)


@app.route('/runService/<string:DpmiStreams>', methods = ['GET'])
def start_process(DpmiStreams):
        data_file=open('/home/ats/working/log.txt','w+')
        data_file.write("Streams being analysed are: \n")
        data_file.write(DpmiStreams)
        data_file.close()
        Dpmi = DpmiStreams.split('_')
        DpmiStreams = ' '.join(Dpmi)
        p = Process(target = start_thread(DpmiStreams))
        p.start()
        return "TCP round trip time analysis has started \n"
@app.route('/button/')
def button_clicked():
    print('Hello world!', file=sys.stderr)
    return sys.stderr()

@app.route('/showData/<string:No>', methods = ['GET'])
def show_data(No):
        cpu=subprocess.check_output("curl -G http://localhost:8086/query --data-urlencode 'u=admin' --data-urlencode 'p=admin' --data-urlencode 'pretty=true' --data-urlencode 'db=five_elements' --data-urlencode 'q=SELECT * FROM TCP_RTT ORDER BY DESC LIMIT '" +No,shell=True)
        dict={}
        gg=[]
        for item in cpu:
                gg.append(cpu)
        dict['data'] = gg[len(gg)-1]
        return dict['data']

@app.route('/stopservice', methods=['GET'])
def stopservice():
         data_file=open('/home/ats/working/log.txt','w+')
         data_file.write('Service Terminated')
         os.system("kill -9 $(pgrep cap2pcap)")
         return "exitFlag changed"


@app.route('/getStatus',methods=['GET'])
def status():
       return send_file('/home/ats/working/log.txt',attachment_filename='log.txt')

@app.route('/AddStream/<string:NewStream>', methods=['GET'])
def add_stream(NewStream):
       oldstreams = open('/home/ats/working/log.txt','r')
       lines = oldstreams.readlines()
       line1 = lines[-1]
       data_file=open('/home/ats/working/log.txt','a')
       data_file.write('_')
       data_file.write(NewStream)
       try:
           stopservice()
           time.sleep(5)
           start_process(line1+' '+NewStream)
       except:
           print ("")
       return "added new stream \n"

@app.route('/DeleteStream/<string:DelStream>', methods=['GET'])
def delete_stream(DelStream):
        oldstreams = open('/home/ats/working/log.txt','r')
        lines = oldstreams.readlines()
        line1 = lines[-1]
        if DelStream in line1:
             NewStream = line1.replace(DelStream,'')
             try:
                 stopservice()
                 time.sleep(5)
                 start_process(NewStream)
             except:
                 print ("")
             return "deleted stream \n"
        else :
             return "stream not present \n"

@app.route('/ChangeStreams/<string:NewStream>', methods=['GET'])
def new_stream(NewStream):
             stopservice()
             time.sleep(1)
             start_process(NewStream)
             return "Changed Streams\n"

def start_thread(DpmiStreams):
        DpmiStream = myThread(DpmiStreams)
        DpmiStream.start()
        return "Stream is being analysed \n"


def start_service(DpmiStreams):
        os.system("stdbuf -o0 cap2pcap -i eth1 "+DpmiStreams+" |stdbuf -o0 tshark -r - -Tfields -e ip.src -e tcp.srcport -e ip.dst -e tcp.dstport -e tcp.analysis.ack_rtt -e frame.time_epoch | stdbuf -o0 python /home/ats/flask-api/awkcpy1.py")

class myThread(threading.Thread):
        def __init__(self,DpmiStreams):
              super(myThread, self).__init__()
              self.DpmiStreams = DpmiStreams

        def run(self):
            start_service(self.DpmiStreams)


if __name__=='__main__':
       app.run(host ='0.0.0.0')

