import json
import logging
from typing import Callable, List

from paho.mqtt.client import Client, MQTTMessage

from tb_vendor.utils import Singleton

logger = logging.getLogger(__name__)

RPC_RESPONSE_TOPIC = 'v1/devices/me/rpc/response/'
RPC_REQUEST_TOPIC = 'v1/devices/me/rpc/request/'
# In order to publish client-side device attributes to ThingsBoard server node,
# send PUBLISH message to the following topic:
# and In order to subscribe to shared device attribute changes, send SUBSCRIBE message to the following topic:
ATTRIBUTES_TOPIC = 'v1/devices/me/attributes'
# Request attribute values from the server
ATTRIBUTES_TOPIC_REQUEST = 'v1/devices/me/attributes/request/'
ATTRIBUTES_TOPIC_RESPONSE = 'v1/devices/me/attributes/response/'
TELEMETRY_TOPIC = 'v1/devices/me/telemetry'
CLAIMING_TOPIC = 'v1/devices/me/claim'
PROVISION_TOPIC_REQUEST = '/provision/request'
PROVISION_TOPIC_RESPONSE = '/provision/response'
RESULT_CODES = {
    1: "incorrect protocol version",
    2: "invalid client identifier",
    3: "server unavailable",
    4: "bad username or password",
    5: "not authorised",
}


def callback_on_connect(client: Client, userdata: dict, flags: dict, rc: int) -> None:
    if rc == 0:
        logger.info("Client Connected to ThingsBoard")
        client.subscribe(f"{RPC_REQUEST_TOPIC}+")
        client.subscribe(ATTRIBUTES_TOPIC)
        client.subscribe(f"{ATTRIBUTES_TOPIC_RESPONSE}+")
        client.subscribe(RPC_RESPONSE_TOPIC + '+')
    else:
        logger.info(f"Client Cannot connect to ThingsBoard, result: {RESULT_CODES[rc]}")


def callback_on_message(client: Client, userdata: dict, msg: MQTTMessage) -> None:
    """on_message callback.

    Responsability:
    - Parse message from ThingsBoard
    """
    logger.debug(f"msg.topic: {msg.topic}")
    payload = json.loads(msg.payload)
    logger.debug(f"msg.payload: {payload}")

    # # Parse the message
    # message_parser(payload, userdata)
    # cmd_parse(payload, userdata)
    # device_attributes(payload, userdata)


class TbMqttConnection:
    def __init__(self, host: str, port: int, keepalive: int = 60):
        self.host = host
        self.port = port
        self.keepalive = keepalive

    def configure_client(self, *, user_data: dict = None,
                         on_connect: Callable = callback_on_connect,
                         on_connect_fail: Callable = None,
                         on_disconnect: Callable = None,
                         on_message: Callable = callback_on_message,
                         on_publish: Callable = None,
                         on_unsubscribe: Callable = None) -> Client:
        if user_data is None:
            user_data = {}
        mqtt_client = Client(userdata=user_data)
        mqtt_client.on_connect = on_connect
        mqtt_client.on_connect_fail = on_connect_fail
        mqtt_client.on_disconnect = on_disconnect
        mqtt_client.on_message = on_message
        mqtt_client.on_publish = on_publish
        mqtt_client.on_unsubscribe = on_unsubscribe
        return mqtt_client


class TbDeviceMqttHandler(Singleton):

    mqtt_clients: List[Client] = []

    def append_mqtt_client(self, client: Client) -> None:
        self.mqtt_clients.append(client)

    def disconnect_all(self):
        for client in self.mqtt_clients:
            client.loop_stop()
            client.disconnect()

    def __len__(self):
        return len(self.mqtt_clients)
