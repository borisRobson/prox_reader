import paho.mqtt.client as mqtt
import sys
from time import sleep
from datetime import datetime
import json
import uuid

MQTT_HOST = "10.10.40.118"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "topic0"
MQTT_MSG = ""
MQTT_QOS = 1
msg = ""
num = str( uuid.uuid1())

def on_connect(mosq, obj, rc):
	print ("Connected to broker : "+ str(rc))
#	do_publish("hello from connected")
	print "Starting"

#def on_publish(client,userdata,mid):
#	print "message published"

def do_publish(msg):
	mqttc.publish(MQTT_TOPIC, msg, MQTT_QOS)

mqttc = mqtt.Client()

#mqttc.on_publish = on_publish
mqttc.on_connect = on_connect

mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_start()

i = 0
now = datetime.now().time()
while i < 600001:
#	global json_string
#	json_string = '{"uid":num,"id":str(i)}'
	json_string = '{"uid":"' + num + '","id":"' + str(i) + '","time":"' + str(datetime.now().time()) + '" }'
#	print json_string
	do_publish(json_string)
	if i == 1:
		print json_string
		print sys.getsizeof(json_string)
		
	i += 1
	sleep (0.001)

print "done"
fin = datetime.now().time()
print("started @ "+ str(now) + " , sent " + str(i) + " messages.")
print("finish time: " + str(fin))
mqttc.disconnect()
	


