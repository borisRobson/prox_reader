import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import paho.mqtt.client as mqtt
import json
from datetime import datetime

MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "readerTopic"

#defne mqtt callbacks
def on_connect(mosq, obj, rc):
	print "connected to mqtt broker"

def on_publish(client, userdata, mid):
	print "message published"

def on_subscribe(mosq, obj, mid, granted_qos):
	print("Subscribed: " + str(mid) + " " + str(granted_qos))

mqttc = mqtt.Client()

mqttc.on_publish = on_publish
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.username_pw_set('ziuhykxg','TjjJgbP0Ojuy')
mqttc.connect("m21.cloudmqtt.com", 14408)
mqttc.subscribe(MQTT_TOPIC,2)

#configure rpi pinout
data_pin = 14
clock_pin = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(data_pin, GPIO.IN)
GPIO.setup(clock_pin, GPIO.IN)

#on every rising edge, detect pin state
def data_callback(channel):
	if GPIO.input(data_pin):
		data.append(0)
	else:
		data.append(1)

def parseKeypad():	
	print "parsing..."	
	#print len(data)
	i = 0
	c = data[i]

	#cycle through array until first '1' bit
	while c != 1:
		i += 1
		c = data[i]

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

	#print reader_value
	reader_index = 0
	stx = 0
	etx = 0

	#get the index of data start and stop
	while reader_index != len(reader_value):
		if etx != 0:
			break
		if reader_value[reader_index] == 11:
			stx = reader_index + 1
		elif reader_value[reader_index] == 15:
			etx = reader_index 
		reader_index += 1
			
	#concat int array to string
	token = ''.join(str(x) for x in  reader_value[stx:etx])
	sendMessage(token)

def sendMessage(token):	
	print "sending..."
	global msg	
	#get datetime, filter off milliseconds
	now = str(datetime.now().time())
	time, ms = now.split('.')
	#create json message object	
	msg = json.dumps({"doorNum":"1","tokenId":token,"time":time}) 
	print msg
	mqttc.publish(MQTT_TOPIC, msg)

def wait_for_input():
	print "waiting..."
	global data
	data = []
	GPIO.wait_for_edge(clock_pin, GPIO.RISING)			
	GPIO.add_event_detect(clock_pin, GPIO.RISING, callback=data_callback)
	sleep(0.75)
	parseKeypad()

print "Ready for input"
rc = 0
while rc == 0:	
	rc = mqttc.loop()
	GPIO.remove_event_detect(clock_pin)
	wait_for_input()

print "Cleaning up..."
mqttc.disconnect()
GPIO.cleanup()