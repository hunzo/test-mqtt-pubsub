import paho.mqtt.client as mqtt
from fastapi import FastAPI

app = FastAPI()

host = "10.100.100.220"
port = 1883
keepAlive = 60


def on_connect(client, userdata, flags, rc):
    print(f"Connect with result {rc}")
    client.subscribe("test/count")


def on_message(client, userdata, msg):
    print(f"Messages body: {msg.payload}")


def on_subscribe(mosq, obj, mid, granted_qos):
    print(f"Subscribed with Qos: {granted_qos}")


def on_publish(client, userdata, mid):
    print(f"Publish ... {mid}")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_publish = on_publish
client.username_pw_set(username="mosquitto", password="mosquitto")
client.connect(host=host, port=port, keepalive=keepAlive)
client.loop_start()


@app.get("/start")
async def app_start():
    client.publish("api/control", "start")
    ret = {
        "server status": "Publish Messages start"
    }
    return ret


@app.get("/stop")
async def app_stop():
    client.publish("api/control", "stop")
    ret = {
        "server status": "Publish Messages stop"
    }
    return ret
