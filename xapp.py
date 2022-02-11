import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

HOST = "10.100.100.220"
PORT = 1883
KEEPALIVE = 60


def on_connect(client, userdata, flags, rc):
    print("on_connect()")
    print(f"Connect result code {rc}")
    print(f"userdata: {userdata}")
    print(f"flags: {flags}")
    client.subscribe("sub/test")


def on_message(client, userdata, msg):
    print("on_message()")
    print(f"message topic: {msg.topic}")
    print(f"client: {client}")
    print(f"userdata: {userdata}")


def on_subscribe(mosq, obq, mid, granted_qos):
    print(f"Subscribe with Qos: {granted_qos}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.username_pw_set(username="mosquitto", password="mosquitto")
# client.connect(host=HOST, port=PORT, keepalive=KEEPALIVE)
client.connect(host=HOST, port=PORT)
# client.loop_start()
