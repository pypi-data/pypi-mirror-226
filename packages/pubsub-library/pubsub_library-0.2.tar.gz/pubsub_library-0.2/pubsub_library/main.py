from pubsub_library.repositories.rabbitmq import RabbitMQPubSub
import asyncio


class PubSubUseCase:
    def __init__(self, pubsub: RabbitMQPubSub):
        self.__pubsub = pubsub

    async def __receive(self, message: bytes):
        print(message)

    async def publish(self, queue_name: str, message: bytes):
        await asyncio.sleep(2)
        async with self.__pubsub:
            await self.__pubsub.publish(queue_name, message)

    async def subscribe(self, queue_name: str):
        async with self.__pubsub:
            await self.__pubsub.subscribe(queue_name, self.__receive)


if __name__ == "__main__":
    rabbitmq = RabbitMQPubSub("amqp://guest:guest@127.0.0.1:5672")
    usecase = PubSubUseCase(rabbitmq)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        asyncio.gather(
            usecase.subscribe("test"), usecase.publish("test", b"Hello World!")
        )
    )
