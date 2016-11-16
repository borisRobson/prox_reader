import sys
import csv
import threading
import signal
import time
from time import sleep
from datetime import datetime
import json
import paho.mqtt.client as mqtt

#define broker settings
MQTT_HOST = 'm21.cloudmqtt.com'
MQTT_PORT = 14408
MQTT_USER = 'ziuhykxg'
MQTT_PW = 'TjjJgbP0Ojuy'
MQTT_TOPIC = "/test/datatest"
MQTT_QOS = 1
MQTT_KEEPALIVE_INTERVAL = 5

#define mqtt callbacks
def on_connect(mosq, obj, rc):
#	print("Connected to broker: " +str(rc))
	mqttc.subscribe([(MQTT_TOPIC, MQTT_QOS), ("/testfinished",1)])

def on_subscribe(mosq, obj, mid, granted_qos):
	print "subcribed to topics"

def handler(signum, frame):
	end = datetime.now().time()
	msg = ("Finished at {0}".format(end))
	mqttc.loop_stop()
	raise Exception(msg)

def device_finished(id):
	devices.append(id)
	if (len(devices) == 3):
		print "Received all finishes"
		signal.alarm(1)

def on_message(mosq, obj, msg):
	if(msg.topic == MQTT_TOPIC):
		rec_time = str(datetime.now().time())
		ms = rec_time[8:]
		unix = int(time.time())
		total = str(unix) + ms
		data = json.loads(msg.payload)	
		data['rec_time'] = str(total)		
		messages.append(data)
	elif(msg.topic == "/testfinished"):
		device_finished(msg.payload)		

def main_loop():
	while run:
		mqttc.loop()

def init():
	global mqttc, messages, devices
	global run

	messages = []
	devices = []

	start = datetime.now().time()
	print "Starting at {0}".format(str(start))

	mqttc = mqtt.Client()
	mqttc.on_connect = on_connect
	mqttc.on_subscribe = on_subscribe
	mqttc.on_message = on_message

	mqttc.username_pw_set(str(MQTT_USER), str(MQTT_PW))
	mqttc.connect(str(MQTT_HOST), MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


def write_file():
	print "Writing File"
	with open('10m.csv', 'w') as mycsvfile:
		fieldnames = ['src', 'msg_id','sent(s)','rec(s)', 'sent full', 'rec full']
		datawriter = csv.writer(mycsvfile ,delimiter=' ', quotechar=',', quoting=csv.QUOTE_MINIMAL)
		for msg in messages:
#			print msg
			sent_time = str(msg['sent_time'])
#			sent = sent_time[6:]
			rec_time = str(msg['rec_time'])
#			rec = rec_time[6:]
			data = '{0},{1},{2},{3}'.format(msg['src'], msg['msg_id'],\
			sent_time, rec_time)
#			print data
			datawriter.writerow(data)


signal.signal(signal.SIGALRM, handler)

class msgThread(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		while exitFlag == 0:
			print "Starting: " + self.name
			main_loop()
			print "Exiting: " + self.name


if __name__=='__main__':
	init()	
	mqttThread = msgThread(1, "mqttThread")
	mqttThread.daemon = True

	global exitFlag
	global run
	exitFlag = 0
	run = True
	mqttThread.start()

	try:
		while True:
			pass
	except Exception, exc:	
		print exc
	finally:
		exitFlag = 1
		run = False
		write_file()
#		print messages
		sys.exit()
