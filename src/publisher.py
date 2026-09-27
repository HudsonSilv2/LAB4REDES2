import argparse
import json
import random
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


BROKER_HOST = "localhost"
BROKER_PORT = 1883


def create_message(device_id: str, qos: int) -> dict:
    return {
        "device_id": device_id,
        "temperature": round(random.uniform(20.0, 35.0), 2),
        "status": "online",
        "qos": qos,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Simulated IoT temperature sensor"
    )

    parser.add_argument(
        "--device-id",
        default="sensor-01",
        help="Device identifier",
    )

    parser.add_argument(
        "--qos",
        type=int,
        choices=[0, 1],
        default=0,
        help="MQTT QoS level",
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=2,
        help="Publishing interval in seconds",
    )

    args = parser.parse_args()

    topic = f"iot/temperature/{args.device_id}"

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=args.device_id,
    )

    print(f"Connecting to MQTT broker {BROKER_HOST}:{BROKER_PORT}...")

    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_start()

    print("Connected.")
    print(f"Device: {args.device_id}")
    print(f"Topic: {topic}")
    print(f"QoS: {args.qos}")
    print(f"Interval: {args.interval}s")
    print("-" * 50)

    try:
        while True:
            message = create_message(args.device_id, args.qos)

            payload = json.dumps(message)

            result = client.publish(
                topic,
                payload,
                qos=args.qos,
            )

            if args.qos > 0:
                result.wait_for_publish()

            print(
                f"[PUBLISHED] "
                f"device={message['device_id']} "
                f"temperature={message['temperature']}°C "
                f"qos={args.qos}"
            )

            print(payload)
            print("-" * 50)

            time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nStopping sensor...")

    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
