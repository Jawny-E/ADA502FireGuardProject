import logging
import queue
import signal
import paho.mqtt.client as paho
from paho import mqtt
import os

# Basic logging setup
logging.basicConfig(filename='subscriber_client.log',
                    format="%(asctime)s [%(levelname)s]: %(message)s", encoding='utf-8',
                    level=logging.DEBUG)

logging.info("MQTT Subscriber Client module")


class SubscriberClient:

    def __init__(self, location_name):
        self.BROKER_HOST = os.environ['BROKER_HOST']
        self.BROKER_PORT = int(os.environ['BROKER_PORT'])
        self.BROKER_TOPIC = os.environ['BROKER_TOPIC']
        self.USERNAME = os.environ['BROKER_USERNAME']
        self.PASSWORD = os.environ['BROKER_PASSWORD']
        self.CLIENT_ID = "PublisherClient"
        self.TOPIC_QOS = 1

        # Initialize the MQTT client
        self.subscriber = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION2,
                                      client_id=self.CLIENT_ID, userdata=None, protocol=paho.MQTTv5)

        # Setup internal message queue
        self.msg_queue = queue.Queue()
        self.do_continue = True
        self.QUEUE_GET_TIMEOUT = 30

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logging.info(f"on_connect: CONNACK {rc}")

    def on_subscribe(self, client, userdata, mid, granted_qos, properties=None):
        logging.info(f"on_subscribe: {mid} {granted_qos}")

    def on_message(self, client, userdata, msg):
        logging.info(f"on_message: {msg.topic} {msg.qos} {msg.payload}")
        self.msg_queue.put(msg.payload)

    def subscriber_start(self):
        self.subscriber.on_message = self.on_message
        self.subscriber.on_connect = self.on_connect
        self.subscriber.on_subscribe = self.on_subscribe

        # Enable TLS for secure connection
        self.subscriber.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        # Set username and password
        self.subscriber.username_pw_set(self.USERNAME, self.PASSWORD)

        # Connect to the broker
        self.subscriber.connect(self.BROKER_HOST, self.BROKER_PORT)

        # Subscribe to the topic
        self.subscriber.subscribe(self.BROKER_TOPIC, qos=self.TOPIC_QOS)
        logging.info(f"Subscribed to topic: {self.BROKER_TOPIC}")

        self.subscriber.loop_start()

    def stop(self):
        self.do_continue = False

    def interrupt_handler(self, *args):
        logging.info("Subscriber client interrupted ...")
        self.do_continue = False

    def process_one(self, in_message):
        # Process the incoming message (override this method for custom behavior)
        logging.info(f"Processing message: {in_message.decode('utf-8')}")

    def process(self):
        while self.do_continue:
            try:
                logging.info("SubscriberClient [Queue:wait]")
                in_message = self.msg_queue.get(timeout=self.QUEUE_GET_TIMEOUT)
                logging.info(f"SubscriberClient [Queue:got] {in_message}")
                self.process_one(in_message)
            except queue.Empty:
                logging.info("SubscriberClient [Queue:empty]")

    def run(self):
        signal.signal(signal.SIGINT, self.interrupt_handler)
        logging.info("Starting subscriber client ...")
        self.subscriber_start()
        self.process()
        logging.info("Stopping subscriber client ...")
        self.subscriber.loop_stop()
        logging.info("Stopped subscriber client ...")


if __name__ == '__main__':
    # Example usage
    location = "Bergen"
    subscriber_client = SubscriberClient(location)
    subscriber_client.run()
   