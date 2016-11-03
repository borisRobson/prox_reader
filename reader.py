import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import paho.mqtt.client as mqtt

MQTT_HOST="10.10.40.137"
MQTT_PORT=1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "readerTopic"

data_pin = 14
clock_pin = 2

GPIO.setmode(GPIO.BCM)
#data pin
GPIO.setup(data_pin, GPIO.IN)
#clock pin
GPIO.setup(clock_pin, GPIO.IN)

data = []

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

GPIO.cleanup()

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

while i != len(data):
	data_byte = data[i: i+value_len]
	out = 0
	index = len(data_byte)

	while index != 0:
		out = (out << 1) | data_byte[index-1]
		index -= 1	
	
#	print out
#	print data_byte

	i += byte_len
	reader_value.append(out)

print reader_value

def on_connect(mosq, obj, rc):
	print "connected to mqtt broker"

def on_publish(client, userdata, mid):
	print "message published"

mqttc = mqtt.Client()

mqttc.on_publish = on_publish
mqttc.on_connect = on_connect

mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

msg = ','.join(str(x) for x in  reader_value)

mqttc.publish(MQTT_TOPIC, msg)

mqttc.disconnect()
