import paho.mqtt.client as mqtt

host = "10.100.100.220"
port = 1883
keepAlive = 60


def on_connect(client, userdata, flags, rc):
    print(f"Connect with result {rc}")
    client.subscribe("test/fromapi")


def on_message(client, userdata, msg):
    print(f"Messages body: {msg.payload}")


def on_subscribe(mosq, obj, mid, granted_qos):
    print(f"Subscribed with Qos: {granted_qos}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.connect(host=host, port=port, keepalive=keepAlive)
client.username_pw_set(username="mosquitto", password="mosquitto")
client.loop_forever()
# client.loop_start()
