import json

import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "iot/temperature/+"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker.")
        print(f"Subscribed to: {TOPIC}")

        client.subscribe(TOPIC, qos=1)

    else:
        print(f"Connection failed: {reason_code}")


def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())

        print("-" * 50)
        print("EVENT RECEIVED")
        print(f"Topic: {message.topic}")
        print(f"Device: {payload['device_id']}")
        print(f"Temperature: {payload['temperature']} °C")
        print(f"Status: {payload['status']}")
        print(f"Publisher QoS: {payload.get('qos')}")
        print(f"Delivered QoS: {message.qos}")
        print(f"Timestamp: {payload['timestamp']}")

        process_event(payload)

    except json.JSONDecodeError:
        print("Invalid JSON received.")

    except KeyError as error:
        print(f"Missing field: {error}")


def process_event(event: dict):
    temperature = event["temperature"]

    if temperature >= 30:
        print("Processing result: HIGH TEMPERATURE ALERT")
    else:
        print("Processing result: Temperature normal")


def main():
    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="temperature-consumer",
    )

    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to {BROKER_HOST}:{BROKER_PORT}...")

    client.connect(BROKER_HOST, BROKER_PORT, 60)

    try:
        client.loop_forever()

    except KeyboardInterrupt:
        print("\nStopping consumer...")

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
