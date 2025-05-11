import json
import logging
import paho.mqtt.client as paho
from paho import mqtt
from paho.mqtt.client import MQTT_ERR_SUCCESS
import requests as request
from fireguard_app.db_locations.database import DatabaseClient
import os
import time

# Basic logging setup
logging.basicConfig(filename='publisher_client.log',
                    format="%(asctime)s [%(levelname)s]: %(message)s", encoding='utf-8',
                    level=logging.DEBUG)

logging.info("MQTT Publisher Client module")

myClient = DatabaseClient(
    username=os.environ['MONGO_DB_USERNAME'],
    password=os.environ['MONGO_DB_PASSWORD'],
    cluster_url="fireguardproject.ggfqm.mongodb.net",
    database_name="FireGuardProject",
    collection_name="location"
)

class PublisherClient:

    def __init__(self):
        # Hardcoded configuration values
        self.BROKER_HOST = os.environ['BROKER_HOST']
        self.BROKER_PORT = int(os.environ['BROKER_PORT'])
        self.BROKER_TOPIC = os.environ['BROKER_TOPIC']
        self.USERNAME = os.environ['BROKER_USERNAME']
        self.PASSWORD = os.environ['BROKER_PASSWORD']
        self.CLIENT_ID = "PublisherClient"
        self.TOPIC_QOS = 1

        self.API_BASE_URL = os.environ['API_BASE_URL']
        self.bearer_token = None
        
        # Initialize the MQTT client
        self.publisher = paho.Client(callback_api_version=paho.CallbackAPIVersion.VERSION2,
                                     client_id=self.CLIENT_ID, userdata=None, protocol=paho.MQTTv5)

        # Keycloak configuration
        self.KEYCLOAK_URL = "http://localhost:8080/realms/FireGuard/protocol/openid-connect/token"
        self.KEYCLOAK_CLIENT_ID = "FireGuardAPI"
        self.KEYCLOAK_USERNAME = "test"
        self.KEYCLOAK_PASSWORD = "testing"
        self.KEYCLOAK_GRANT_TYPE = "password"
        # Enable TLS for secure connection
        self.publisher.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

        # Set username and password
        self.publisher.username_pw_set(self.USERNAME, self.PASSWORD)

        # Assign callbacks
        self.publisher.on_connect = self.on_connect
        self.publisher.on_publish = self.on_publish

    def get_bearer_token(self):
        """
        Authenticate with Keycloak and retrieve a bearer token.
        """
        data = {
            "client_id": self.KEYCLOAK_CLIENT_ID,
            "username": self.KEYCLOAK_USERNAME,
            "password": self.KEYCLOAK_PASSWORD,
            "grant_type": self.KEYCLOAK_GRANT_TYPE
        }
        try:
            response = request.post(self.KEYCLOAK_URL, data=data)
            if response.status_code == 200:
                token_data = response.json()
                self.bearer_token = token_data["access_token"]
                logging.info("Successfully obtained bearer token.")
            else:
                logging.error(f"Failed to obtain bearer token. Status code: {response.status_code}, Response: {response.text}")
        except request.RequestException as e:
            logging.error(f"Error connecting to Keycloak: {e}")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            logging.info("Connected to HiveMQ broker successfully!")
        else:
            logging.error(f"Failed to connect, return code {rc}")

    def on_publish(self, client, userdata, mid, reason_code, properties=None):
        logging.info(f"Message {mid} published successfully with reason code {reason_code}")

    def fetch_fire_risk(self, location_name):
        """Fetch fire risk data from the API for a given location."""

        if not self.bearer_token:
            self.get_bearer_token()

        headers = {
            "Authorization": f"Bearer {self.bearer_token}"
        }
        api_url = f"{self.API_BASE_URL}{location_name}"
        try:
            response = request.get(api_url, headers=headers)
            if response.status_code == 200:
                logging.info(f"Fetched fire risk data for {location_name}. Status code: {response.status_code}")
                return response.json()
            else:
                logging.error(f"Failed to fetch fire risk data for {location_name}. Status code: {response.status_code}")
                return None
        except request.RequestException as e:
            logging.error(f"Error fetching fire risk data for {location_name}: {e}")
            return None
        
    def publish_daily_updates(self, delay_between_locations=0.5):
        logging.info("Publisher client connecting ...")

        locations = myClient.collection.find()

        # Connect to the broker
        self.publisher.connect(self.BROKER_HOST, self.BROKER_PORT)
        self.publisher.loop_start()

        logging.info("Publisher client connected ...")

        for location in locations:
            location_name = location.get("name")
            fire_risk_data = self.fetch_fire_risk(location_name)

            if fire_risk_data:
                topic = f"fireguard/updates/{location_name}"
                message = json.dumps(fire_risk_data)

                # Publish the message
                result = self.publisher.publish(topic, payload=message, qos=self.TOPIC_QOS)

                # Wait for the message to be published
                if result.rc == MQTT_ERR_SUCCESS or result.is_published():
                    result.wait_for_publish(60)
                    logging.info(f"Published fire risk update for {location_name} to topic {topic}")
                else:
                    logging.error(f"Failed to publish update for {location_name}")

        # Stop the loop
        self.publisher.loop_stop()
        self.publisher.disconnect()


if __name__ == "__main__":
# Create an instance of the PublisherClient
    publisher_client = PublisherClient()

    # Call the method to publish daily updates  
    try:
        publisher_client.publish_daily_updates()
        logging.info("Publisher ran successfully.")
    except Exception as e:
        logging.error(f"An error occurred while running the publisher: {e}")