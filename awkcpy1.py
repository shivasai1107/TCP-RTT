#!usr/bin/python -u
import sys
from influxdb import InfluxDBClient
import os
import time
import datetime

client=InfluxDBClient('localhost',8086,'admin','admin',database='five_elements')
def feed(tcptuple,rtt,time):
      json_body=[
              {
              "measurement":"TCP_RTT",
              "tags":{
                      "stream":tcptuple
                       },
                       "time":time,
                       "fields":{
                               "rtt":rtt

                       }
      }
      ]
      client.write_points(json_body,time_precision='u')
f = os.fdopen(sys.stdin.fileno(),'r',0)
for line in f:
    fields = line.strip().split()
    if len(fields) == 6:
        print line
        a = ":".join([fields[0],fields[1]])
        b = ":".join([fields[2],fields[3]])
        c = ",".join([a,b])
        ut = fields[5].split('.')
        st = datetime.datetime.utcfromtimestamp(long(float(ut[0]))).strftime('%Y-%m-%dT%H:%M:%S')
        pt = ".".join([st,ut[1]])
        feed(c,float(fields[4]),pt)
        print (c , fields[4],pt)

