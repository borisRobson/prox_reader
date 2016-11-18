import sys
import signal
import time
from time import sleep
from datetime import datetime
import json
import paho.mqtt.client as mqtt

DEVICE_ID = str(1)

#define broker settings
MQTT_HOST = "10.10.40.118"
MQTT_PORT = 1883
MQTT_USER = 'ziuhykxg'
MQTT_PW = 'TjjJgbP0Ojuy'
MQTT_TOPIC = "/test/datatest"
MQTT_QOS = 0
MQTT_KEEPALIVE_INTERVAL = 5

RATE = 2
DURATION = 600
TOTAL = RATE * DURATION

#define mqtt callbacks
def on_connect(mosq, obj, rc):
	print ("Connected to broker: " +str(rc))
	
def on_publish(client, userdata,mid):
	sent = int(mid)
	if (sent == TOTAL):
		print("sending finish")
		mqttc.publish("/testfinished",DEVICE_ID,2)
	if(sent == TOTAL + 1):
		print("finishing")
		signal.alarm(1)		

def publish_msg(msg):
	mqttc.publish(MQTT_TOPIC, msg, MQTT_QOS)

#create client instance and connect to broker
def init():
	global mqttc
	mqttc = mqtt.Client()
	mqttc.on_connect = on_connect
	mqttc.on_publish = on_publish
	mqttc.username_pw_set(str(MQTT_USER), str(MQTT_PW))
	mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
	mqttc.loop_start()

#handler to exit loop
def handler(signum, frame):
	end = datetime.now().time()
	msg = ("Finsihed at {0}".format(end))
	raise Exception(msg)

#method to create json payload
def create_msg(msg_id):
	timestamp = str(datetime.now().time())
	ms = timestamp[8:]
	unix = int(time.time())
	total = str(unix) + ms
	msg = {
		'sent_time':'{0}'.format(total),
		'src': '{0}'.format(DEVICE_ID),
		'msg_id':'{0}'.format(str(msg_id)),
		'rec_time':' '
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
		sleep(0.5)

signal.signal(signal.SIGALRM, handler)
	

if __name__=="__main__":
	init()
	start = datetime.now().time()
	print "Starting at {0}".format(str(start))
#	signal.alarm(10)
	try:
		while 1:
			msg_loop()
	except Exception,exc:
#		mqttc.publish("/testfinished", DEVICE_ID,1)
		print exc
		mqttc.loop_stop()
		sys.exit()
	
