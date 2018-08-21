## Prototype for thermo.py
##

import network

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
# sta_if.connect("elfhome", "--password--")
if sta_if.isconnected() is False:
    print("You must connect the WiFi first.")

import machine
import bme280
import ujson
import utime
from umqtt.simple import MQTTClient

MQTT_CLIENT_NAME = b"esp8255_test"
MQTT_SRV_IP = "10.3.4.169"  # host: infux.elfwerks
MQTT_LOG_TOPIC = "elfwerks/stoneglen/log"
MQTT_TOPIC  = "elfwerks/stoneglen/env"

## Initialize the BME280
##

MY_SCK = 5   ## GPIO-5 = D1  -- wiring dependent
MY_SDI = 4   ## GPIO-4 = D2  -- wiring dependent

MY_BME280_ADDR = 0x77  ## nor sure why this shows up with _this_ addr.

i2c = machine.I2C( scl = machine.Pin(MY_SCK),
                   sda = machine.Pin(MY_SDI) )
bme = bme280.BME280( address = MY_BME280_ADDR,
                     i2c = i2c )

## Connect to MQTT
##
print("connecting to: "+MQTT_SRV_IP)
client = MQTTClient(MQTT_CLIENT_NAME, MQTT_SRV_IP)
client.connect()

client.publish(MQTT_LOG_TOPIC, 'proto-thermo starting')

## Go to work.
##
count = 600
# while count > 0:
(temp, pres, humid) = bme.values
rec = {
    "temperature" : temp,
    "pressure" : pres,
    "humidity" : humid }
strdata = ujson.dumps(rec)
client.publish(MQTT_TOPIC, strdata)
# utime.sleep(60)
count = count - 1


## Shutdown

client.publish(MQTT_LOG_TOPIC, 'proto-thermo exiting')
client.disconnect()
print("proto-thermo done.")
