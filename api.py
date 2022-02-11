from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
import redis

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

host = "10.100.100.220"
port = 1883
keepAlive = 60

r = redis.Redis(host=host, port=6379, db=1)


def on_connect(client, userdata, flags, rc):
    print(f"Connect with result {rc}")
    client.subscribe("test/count")


def on_message(client, userdata, msg):
    print(f"Messages body: {msg.payload}")
    if str(msg.payload.decode("utf-8")) == "inc":
        print("Call Redis: increase counter")
        r.incr("count")


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


@app.get("/control/start")
async def app_start():
    client.publish("api/control", "start")
    ret = {
        "server status": "Publish Messages start"
    }
    return ret


@app.get("/control/stop")
async def app_stop():
    client.publish("api/control", "stop")
    ret = {
        "server status": "Publish Messages stop"
    }
    return ret


@app.post("/counter/inc")
async def counter_inc():
    r.incr("count")
    ret = {
        "status": "inc"
    }
    return ret


@app.post("/counter/dec")
async def counter_dec():
    r.decr("count")
    ret = {
        "status": "dec"
    }
    return ret


@app.get("/counter/show")
async def counter_show():
    ret = {
        "count": r.get("count")
    }
    return ret


@app.delete("/counter/clear")
async def counter_clear():
    r.delete("count")
    ret = {
        "status": "clear counter"
    }
    return ret
