import paho.mqtt.client as mqtt


def pub(topic: str, message: str):
    host = "10.100.100.220"
    port = 1883

    client = mqtt.Client()
    client.username_pw_set(username="mosquitto", password="mosquitto")
    client.connect(host=host, port=port)
    client.publish(topic, message)


pub("test/count", "test_message")
