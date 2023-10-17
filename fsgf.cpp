import paho.mqtt.client as mqtt
import requests

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("mqtt/topic")
    else:
        print(f"Connection to MQTT broker failed with code {rc}")

def on_message(client, userdata, msg):
    if msg.topic == "mqtt/topic":
        message = msg.payload.decode("utf-8")
        print("your bike got accident :", message)
        # Replace the URL with your IFTTT webhook URL
        requests.post("https://maker.ifttt.com/trigger//6d554g/ankit/dk6s4/fCJ-e_x2TTfn-BQnYlvHzZ4Xk_CGgnQRd4jWLACG4AS", data={"value1": message})

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

mqtt_server = "198.168.43.32"  # Replace with the Raspberry Pi's IP address
mqtt_port = 1883

client.connect(mqtt_server, mqtt_port, 60)
client.loop_forever()