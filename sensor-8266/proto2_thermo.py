## Prototype-2 for thermo.py
##

import bme280
import machine
import network
import ujson
import utime

from umqtt.simple import MQTTClient

## Board Constants

MY_SCK = 5     # GPIO-5 = D1  -- wiring dependent
MY_SDI = 4     # GPIO-4 = D2  -- wiring dependent

MY_BME280_ADDR = 0x77  # not sure why this shows up with _this_ addr.

## ########################################

def bootstrap_network():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if sta_if.isconnected() is False:
        print("You must connect the WiFi first.")
        return False
    return True

def discover(cfg):
    ##
    ## TODO - multicast discovery of services
    ##
    cfg['cfg-server'] = '10.3.4.999:98754'
    return cfg

def get_config(cfg):
    ##
    ## TODO - REST query of the cfg-server
    ##
    cfg['logging'] = {
        'mqtt-topic': 'elfwerks/stoneglen/log',
    }
    cfg['sensor']  = {
        'mqtt-topic': 'elfwerks/stoneglen/env',
        'samp-period': 60,
    }
    cfg['mqtt'] = {
        'client-name': 'esp8255-test',
        'server-addr': '10.3.4.169',  # host: influx.elfwerks
    }
    return cfg

class BME280Sensor():
    def __init__(self):
        self._t = 0
        self._p = 0
        self._h = 0
        i2c = machine.I2C( scl = machine.pin(MY_SCK),
                           sda = machine.pin(MY_SDI) )
        self.bme = bme280.BME280( address = MY_BME280_ADDR,
                                  i2c = i2c )

    def update(self):
        t, p, h = self.bme.read_compensated_data()
        self._t = t / 100  ## Celicus
        self._p = p / 256  ## hPa
        self._h = h / 1024 ## % humidity

    @property
    def temperature():
        return self._t

    @property
    def pressure():
        return self._p

    @property
    def humidity():
        return self._h

def connect_mqtt(cfg):
    client_name = cfg['mqtt']['client-name']
    server_addr = cfg['mqtt']['server-addr']
    client = MQTTClient(client_name, server_addr)
    client.connect()
    return client

class Logger():
    def __init__(self):
        self._q  = []
        self._mq = None

    def set_mq(self, mq, topic):
        self._mq = mq
        self._topic = topic
        while m in self._q:
            self.send(m)

    def _send(self, msg):
        if self._mq:
            self._mq.publish(self._topic, msg)
        else:
            self.fatal('Logger._send() invoked with no mq')

    def log(self, msg):
        if self._mq:
            self._send(msg)
        else:
            self._q.append(msg)

    def fatal(self, msg):
        while True:
            print("FATAL: {}".format(msg))
            utime.sleep(5)

if __name__=='__main__':

    log = Logger()

    if not bootstrap_network():
        log.fatal('network(wifi) not initialized')

    cfg = {}
    cfg = discover(cfg)   ## discover cfg server
    cfg = get_config(cfg) ## load config from cfg server

    mq = connect_mqtt(cfg)
    sensor = BME280Sensor()

    log_topic = cfg['logging']['mqtt-topic']
    log.set_mq(mq, log_topic)
    log.log('proto2-thermo starting')

    rec = {
        'attr': 'Value',    ## ? what values are static?
        'room': 'from-cfg', ## some static vals are from cfg
    }
    topic = cfg['sensor']['mqtt-topic']
    period = int(cfg['sensor']['samp-period'])

    while True:  ## loop forever
        sensor.update()
        rec['temp'] = sensor.temperature
        rec['pres'] = sensor.pressure
        rec['humid'] = sensor.humidity

        msg = ujson.dumps(rec)
        mq.publish(topic, msg)

        utime.sleep(period)

## End of file.
