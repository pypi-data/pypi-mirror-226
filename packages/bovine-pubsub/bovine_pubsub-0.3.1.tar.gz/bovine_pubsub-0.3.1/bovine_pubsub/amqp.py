import logging
import aio_pika

from uuid import uuid4

logger = logging.getLogger(__name__)


class AmqpBovinePubSub:
    def __init__(self, amqp_uri):
        self.amqp_uri = amqp_uri
        self.connection = None

    async def send(self, endpoint_path, data):
        connection = await aio_pika.connect_robust(self.amqp_uri)
        async with connection:
            channel = await connection.channel()

            processed_exchange = await channel.declare_exchange(
                "processed",
                aio_pika.ExchangeType.TOPIC,
            )

            await processed_exchange.publish(
                aio_pika.Message(
                    body=data,
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                ),
                routing_key=endpoint_path,
            )

    async def event_stream(self, endpoint_path):
        connection = await aio_pika.connect_robust(self.amqp_uri)
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=10)
            processed_exchange = await channel.declare_exchange(
                "processed",
                aio_pika.ExchangeType.TOPIC,
            )
            queue = await channel.declare_queue(str(uuid4()), auto_delete=True)
            await queue.bind(processed_exchange, routing_key=endpoint_path)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        body = message.body
                        yield body
                        yield "\n".encode("utf-8")
