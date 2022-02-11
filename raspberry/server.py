#!/usr/bin/python3
import paho.mqtt.client as mqtt
import time
import RPi.GPIO as GPIO
import time


host = "10.100.100.220"
port = 1883
keepAlive = 60

# GPIO
GPIO.setmode(GPIO.BCM)

GPIO_RELAY = 17
GPIO.setup(GPIO_RELAY, GPIO.OUT)

GPIO_SENSOR_1 = 4
GPIO.setup(GPIO_SENSOR_1, GPIO.IN)

GPIO_LED = 2
GPIO.setup(GPIO_LED, GPIO.OUT)

GPIO_COUNT_LED = 3
GPIO.setup(GPIO_COUNT_LED, GPIO.OUT)



DELAY_TIME = 1

def OPEN_RELAY():
    GPIO.output(GPIO_RELAY, False)

def CLOSE_RELAY():
    GPIO.output(GPIO_RELAY, True)

def START_RELAY():
    OPEN_RELAY()

def STOP_RELAY():
    CLOSE_RELAY()

def LED_ON():
    GPIO.output(GPIO_LED, True)

def LED_OFF():
    GPIO.output(GPIO_LED, False)

def LED_COUNT_ON():
    GPIO.output(GPIO_COUNT_LED, True)

def LED_COUNT_OFF():
    GPIO.output(GPIO_COUNT_LED, False)




# CONTROL
CONTROL = 1

def SET_CONTROL():
    global CONTROL
    CONTROL = 0
    LED_ON()

def CLEAR_CONTROL():
    global CONTROL
    CONTROL = 1
    LED_OFF()

def initial():
    STOP_RELAY()
    LED_OFF()
    LED_COUNT_OFF()
    CLEAR_CONTROL()


# MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connect with result {rc}")
    client.subscribe("api/control")

def on_message(client, userdata, msg):
    print(f"Messages body: {msg.payload}")
    control = msg.payload.decode("utf-8")
    print(control)

    if control == "start":
        print("Start RELAY")
        START_RELAY()
        SET_CONTROL()

    if control == "stop":
        print("Stop RELAY")
        STOP_RELAY()
        CLEAR_CONTROL()

def on_subscribe(mosq, obj, mid, granted_qos):
    print(f"Subscribed with Qos: {granted_qos}")

def on_publish(client, userdata, mid):
    print(f"rasp:publish messages {mid}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish
client.connect(host=host, port=port, keepalive=keepAlive)
client.username_pw_set(username="mosquitto", password="mosquitto")
# client.loop_forever()
client.loop_start()
print("Loop Start ....")

def monitor():
    START_RELAY()
    STOP_RELAY()

def CountLoop():
    print("test wait")
    w = True
    while w:
        SENSOR_1 = GPIO.input(GPIO_SENSOR_1)
        print("Count wait......")
        if SENSOR_1 == 1:
            w = False
            print("Count !!!!")
            client.publish("test/count", "inc")
            LED_COUNT_OFF()
            monitor()

if __name__ == "__main__":
    print("Counter Start ....")
    initial()
    try:
        while True:
            SS_1 = GPIO.input(GPIO_SENSOR_1)
            if CONTROL == 0:
                # print("control => 0, ", SS_1, "start")
                if SS_1 == 0:
                    LED_COUNT_ON()
                    CountLoop()
            if CONTROL == 1:
                pass
                # print("control => 1, close")
            time.sleep(0.001)
            # pass
    except KeyboardInterrupt:
        print("Stop")
    finally:
        initial()
        GPIO.cleanup()
