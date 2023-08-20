import json
from bovine.types import ServerSentEvent


class AmqpIterator:
    def __init__(self, queue, clients):
        self.clients = clients
        self.queue = queue.iterator()

    async def __aenter__(self):
        await self.queue.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.queue.__aexit__(exc_type, exc_val, exc_tb)

    def __aiter__(self):
        return self

    async def __anext__(self):
        message = await self.queue.__anext__()

        async with message.process():
            client = self.clients[message.routing_key]
            body = message.body.decode("utf-8")
            event = ServerSentEvent.parse_utf8(body)

        return client, json.loads(event.data)
