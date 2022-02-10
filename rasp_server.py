import paho.mqtt.client as mqtt
import time

host = "10.100.100.220"
port = 1883
keepAlive = 60


def on_connect(client, userdata, flags, rc):
    print(f"Connect with result {rc}")
    client.subscribe("api/control")


def on_message(client, userdata, msg):
    print(f"Messages body: {msg.payload}")
    control = msg.payload.decode("utf-8")
    print(control)

    if control == "start":
        print("yeah start")
    if control == "stop":
        print("yeah stop")


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
while True:
    print("loop start")
    time.sleep(2)
