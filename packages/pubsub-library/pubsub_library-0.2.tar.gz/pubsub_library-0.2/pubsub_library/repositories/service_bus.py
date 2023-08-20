from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from pubsub_library.interfaces.pubsub import PubSubInterface
from typing import Callable
import logging


class AzurePubSub(PubSubInterface):
    def __init__(self, connection_string: str):
        self.__client = ServiceBusClient.from_connection_string(
            connection_string
        )
        self.__logger = logging.getLogger(__name__)

    async def __aenter__(self) -> "AzurePubSub":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        return None

    async def publish(self, queue_name: str, message: bytes):
        try:
            async with self.__client:
                async with self.__client.get_queue_sender(
                    queue_name
                ) as sender:
                    await sender.send_messages(ServiceBusMessage(message))
        except Exception as e:
            self.__logger.error(f"Error sending message: {e}")
            raise Exception("Error sending message")

    async def subscribe(
        self, queue_name: str, callback: Callable[[bytes], None]
    ):
        try:
            async with self.__client:
                async with self.__client.get_queue_receiver(
                    queue_name
                ) as receiver:
                    messages = await receiver.receive_messages(
                        max_message_count=1, max_wait_time=5
                    )
                    for message in messages:
                        await receiver.complete_message(message)
                        await callback(message.body)
        except Exception as e:
            self.__logger.error(f"Error receiving message: {e}")
            raise Exception("Error receiving message")
