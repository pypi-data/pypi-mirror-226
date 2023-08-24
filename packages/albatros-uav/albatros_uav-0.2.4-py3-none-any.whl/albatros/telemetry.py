import logging
from enum import Enum

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pymavlink import mavutil

from .receive_loop import ReceiveLoop
from .uav_data import UAVData

logger = logging.getLogger(__name__)


class ConnectionType(Enum):
    DIRECT = 1
    RABBITMQ = 2


class Telemetry:
    def __init__(
        self,
        connection_type: ConnectionType = ConnectionType.DIRECT,
        device: str = "udpin:0.0.0.0:14550",
        baud_rate: int = 115200,
        host: str = "localhost",
    ) -> None:
        self.direct_connection: mavutil.mavudp
        self.rabbit_connection: BlockingChannel
        self.connection_type = connection_type
        self.device = device
        self.baud_rate = baud_rate
        self.host = host
        self.data = UAVData()

        if self.connection_type == ConnectionType.DIRECT:
            self.make_direct_connection()

        if self.connection_type == ConnectionType.RABBITMQ:
            self.make_rabbitmq_connection()

    def make_direct_connection(self) -> None:
        self.direct_connection = mavutil.mavlink_connection(self.device, self.baud_rate)
        self.direct_connection.wait_heartbeat()
        logger.info("heartbeat recived")

        # starts a thread that receives telemetry
        receive_telem_loop = ReceiveLoop(self.direct_connection, self.data)
        receive_telem_loop.start()

    def make_rabbitmq_connection(self) -> None:
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.rabbit_connection = connection.channel()
        self.rabbit_connection.queue_declare(queue="commands")

    def send(self, message: bytes) -> None:
        if self.connection_type == ConnectionType.DIRECT:
            self.direct_connection.write(message)

        if self.connection_type == ConnectionType.RABBITMQ:
            self.rabbit_connection.basic_publish(
                exchange="", routing_key="commands", body=message
            )
