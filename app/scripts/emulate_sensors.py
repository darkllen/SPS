import asyncio
import aio_pika
import random
import json
from time import sleep

async def send_message():
    p = 100  # number of cities
    s = 1000
    n = 100  # number of messages in sec
    u = 100  # number of users
        
    # Connect to the RabbitMQ server
    connection = await aio_pika.connect_robust(
        host='localhost',
        login='guest',
        password='guest',
        virtualhost='/'
    )
    
    # Create a channel
    channel = await connection.channel()
    
    # Declare a queue
    queue = await channel.declare_queue('events_queue', durable=True)
    # Send messages
    while True:
        # Generate a random id and city
        id = random.randint(1, s)
        city = f'city{id%p}'
        
        # Determine whether the user is logged in or not
        if random.random() < 0.1:
            user_id = None
        else:
            user_id = random.randint(1, u)
        
        # Define the message payload
        message = {
            'id': id,
            'city': city,
            'event_name': random.choice(['locked', 'unlocked']),
            'user_id': user_id
        }

        # Convert the payload to JSON
        message_json = json.dumps(message)
        # Publish the message
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=message_json.encode(),
                content_type='application/json'
            ),
            routing_key='events_queue'
        )
        # return
        # sleep(1/n)


    # Close the connection
    await connection.close()
async def main():

    num_threads = 64  # number of threads to use

    # Create a list of coroutines to run
    coroutines = [send_message() for _ in range(num_threads)]
    
    # Run the coroutines concurrently using asyncio.gather()
    await asyncio.gather(*coroutines)

# Run the script
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
