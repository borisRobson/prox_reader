import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import paho.mqtt.client as mqtt
import json
from datetime import datetime


#MQTT_HOST="10.10.40.137"
#MQTT_PORT=1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "readerTopic"

data_pin = 14
clock_pin = 2

#configure rpi pinout
GPIO.setmode(GPIO.BCM)
#data pin
GPIO.setup(data_pin, GPIO.IN)
#clock pin
GPIO.setup(clock_pin, GPIO.IN)

#create blank array for binary data value
data = []

#on every rising edge, detect pin state
def data_callback(channel):
	if GPIO.input(data_pin):
		data.append(0)
	else:
		data.append(1)

print "Ready for input"

#blocks until data starts
GPIO.wait_for_edge(clock_pin, GPIO.RISING)

#triggers callback on every rising edge
GPIO.add_event_detect(clock_pin, GPIO.RISING, callback=data_callback)

sleep(0.75)

i = 0
c = data[i]

#cycle through array until first '1' bit
while c != 1:
	i += 1
	c = data[i]

#print data[i:]

byte_len = 5
value_len = 4
data_byte = []
reader_value = []

#convert binary to int array
while i != len(data):
	data_byte = data[i: i+value_len]
	out = 0
	index = len(data_byte)

	#reader value is lsb first
	#start at end and work backwards to decode value
	while index != 0:
		out = (out << 1) | data_byte[index-1]
		index -= 1	
	
	#read next data byte
	i += byte_len
	reader_value.append(out)


print reader_value
reader_index = 0
stx = 0
etx = 0

#get the index of data start and stop
while reader_index != len(reader_value):
	if reader_value[reader_index] == 11:
		stx = reader_index + 1
	elif reader_value[reader_index] == 15:
		etx = reader_index 
	reader_index += 1

print etx
print stx
		
#defne mqtt callbacks
def on_connect(mosq, obj, rc):
	print "connected to mqtt broker"

def on_publish(client, userdata, mid):
	print "message published"

mqttc = mqtt.Client()

mqttc.on_publish = on_publish
mqttc.on_connect = on_connect

#mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

mqttc.username_pw_set('ziuhykxg','TjjJgbP0Ojuy')
mqttc.connect("m21.cloudmqtt.com", 14408)

mqttc.subscribe(MQTT_TOPIC,0)

#mqttc.publish("hello/word", "from python on pi")


#concat int array to string
token = ''.join(str(x) for x in  reader_value[stx:etx])

#get datetime, filter off milliseconds
now = str(datetime.now().time())
val, ms = now.split('.')

#create json message object
json = json.dumps({"doorNum":"1","tokenId":token,"time":val}) 

print json

mqttc.publish(MQTT_TOPIC, json)

mqttc.disconnect()
GPIO.cleanup()