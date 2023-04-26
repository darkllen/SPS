import asyncio
import aio_pika
import json
from db.connection import get_session
from db.database import Event, Sensor, SENSOR_STATUS_ENUM
from sqlalchemy.sql import select

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        # Get the message payload as a JSON object
        payload = json.loads(message.body.decode())
        async with get_session() as session:
            res = await session.execute(select(Sensor).filter(Sensor.id == payload['id']))
            sensor = res.scalars().first()
            if not sensor:
                sensor = Sensor(
                        id =payload['id'],
                        city=payload['city'],
                        status = 'available' if payload['event_name']=='unlocked' else 'in_usage',
                )
                session.add(sensor)
        # Process the message
        # print(f'Received message: {payload}')


async def consume():
    # Connect to the RabbitMQ server
    connection = await aio_pika.connect_robust(
        host='rabbitmq',
        login='guest',
        password='guest',
        virtualhost='/'
    )

    # Create a channel
    channel = await connection.channel()

    # Start consuming messages
    await channel.set_qos(prefetch_count=1000)

    # Declaring queue
    queue = await channel.declare_queue('events_queue', durable=True)

    await queue.consume(on_message)
    try:
        # Wait until terminate
        await asyncio.Future()
    finally:
        await connection.close()


# Run the consumer
asyncio.run(consume())
