import paho.mqtt.client as mqtt
import json
from datetime import datetime


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
		id = val['id']		
		print("msgId: " + str(id) +  ",msgtime : " + str(msgtime)+ ",rectime: " + str(rectime))
		print("diff: " + str(diff))
		i += 1
	mqttc.loop_stop()
		
def on_connect(mosq, obj, rc):
	print "Connected to broker"
	mqttc.subscribe(MQTT_TOPIC, 0)

def on_subscribe(mosq, obj, mid, granted_qos):
	print "Subscribed to topic"


def on_message(mosq, obj, msg):
	data.append(str(msg.payload))
	rectimes.append(datetime.now().time())
	i = len(data)
	if(i == 2500):
		check_data()

mqttc = mqtt.Client()

mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
mqttc.loop_forever()

mqttc.disconnect()
