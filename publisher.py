import sys
import signal
import time
from time import sleep
from datetime import datetime
import json
import paho.mqtt.client as mqtt

DEVICE_ID = str(1)

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
	print ("Connected to broker: " +str(rc))

def publish_msg(msg):
	mqttc.publish(MQTT_TOPIC, msg, MQTT_QOS)

#create client instance and connect to broker
def init():
	global mqttc
	mqttc = mqtt.Client()
	mqttc.on_connect = on_connect
	mqttc.username_pw_set(str(MQTT_USER), str(MQTT_PW))
	mqttc.connect(str(MQTT_HOST), MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
	mqttc.loop_start()

#handler to exit loop
def handler(signum, frame):
	end = datetime.now().time()
	msg = ("Finsihed at {0}".format(end))
	raise Exception(msg)

#method to create json payload
def create_msg(msg_id):
	time = datetime.now().time()
	msg = {
		'sent_time':'{0}'.format(time),
		'src': '{0}'.format(DEVICE_ID),
		'msg_id':'{0}'.format(str(msg_id))
		}
	json_msg = json.dumps(msg)
	return json_msg

#main loop
def msg_loop():
	msg_id = 0
	while 1:
		payload = create_msg(msg_id)
		publish_msg(payload)
		msg_id += 1
		sleep(0.1)

signal.signal(signal.SIGALRM, handler)
	

if __name__=="__main__":
	init()
	start = datetime.now().time()
	print "Starting at {0}".format(str(start))
	signal.alarm(1)
	try:
		while 1:
			msg_loop()
	except Exception,exc:
		print "quitting"
		publish_msg("/testfinished", DEVICE_ID)
		print exc
		mqttc.loop_stop()
		sys.exit()
	
