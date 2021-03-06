import paho.mqtt.client as mqtt
import json
from datetime import datetime
import sys

MQTT_HOST = "10.10.40.118"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 5 
MQTT_TOPIC = "testTopic"
global msg_count
msg_count = 0
data = []
rectimes = []

def check_data():
	i = 0
	missed = 0
	while i < (len(data) -1):
		val = json.loads(data[i])
		fullmsgtime = str(val['time'])
		msgtime = fullmsgtime[6:]
		fullrectime = str(rectimes[i])
		rectime = fullrectime[6:]
		diff = float(rectime) - float(msgtime)
		if diff < 0:
			diff += 60.0
		id = val['id']		
#		print("msgId: " + str(id) +  ",msgtime : " + str(msgtime)+ ",rectime: " + str(rectime))
#		print("diff: " + str(diff))
		print(str(id)+","+ str(msgtime)+","+ str(rectime)+ ","+str(diff)) 
		i += 1
	print sys.getsizeof(data[i])
	mqttc.loop_stop()
		
def on_connect(mosq, obj, rc):
#	print "Connected to broker"
	mqttc.subscribe(MQTT_TOPIC, 0)

def on_subscribe(mosq, obj, mid, granted_qos):
#	print "Subscribed to topic"
	print("msgId, sent Time, Rec Time, Diff")


def on_message(mosq, obj, msg):
	data.append(str(msg.payload))
	rectimes.append(datetime.now().time())
	i = len(data)
	if(i == 600000):
		check_data()

mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_forever()

mqttc.disconnect()
