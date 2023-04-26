import asyncio
import aio_pika
import json
from db.connection import get_session
from db.database import Event, Sensor
from sqlalchemy.sql import select
from settings import settings
from enitites.sensor_event import SensorEventMessage, EventName, EventStatus, name_status_map
from datetime import datetime
from uuid import uuid4
import pytz

async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        # Get the message payload as a JSON object
        sensor_event = SensorEventMessage.validate(json.loads(message.body.decode()))
        async with get_session() as session:
            res = await session.execute(select(Sensor).filter(Sensor.id == sensor_event.id))
            sensor = res.scalars().first()
            if not sensor:
                sensor = Sensor(
                        id=sensor_event.id,
                        external_id=str(uuid4()),
                        city=sensor_event.city,
                        status = EventStatus.AVAILABLE if sensor_event.event_name==EventName.UNLOCKED else EventStatus.IN_USAGE,
                )
                session.add(sensor)
                event = Event(
                    event_name = sensor_event.event_name,
                    sensor_external_id = sensor.external_id,
                    data = {
                        "user_id": sensor_event.user_id,
                    }
                )
                session.add(event)
            if sensor.status != name_status_map.get(sensor_event.event_name):
                prev_status = sensor.status
                sensor.status = name_status_map.get(sensor_event.event_name)
                df_time = (datetime.utcnow() - sensor.updated_at).total_seconds()
                session.add(sensor)
                event = Event(
                    event_name = sensor_event.event_name,
                    sensor_external_id = sensor.external_id,
                    data = {
                        "user_id": sensor_event.user_id,
                        f"{prev_status}_s": df_time
                    }
                )
                session.add(event)


        # Process the message
        # print(f'Received message: {payload}')


async def consume():
    # Connect to the RabbitMQ server
    print(settings.rabbit_host)
    connection = await aio_pika.connect_robust(
        host=settings.rabbit_host,
        login=settings.rabbit_user,
        password=settings.rabbit_password,
        port=settings.rabbit_port,
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
