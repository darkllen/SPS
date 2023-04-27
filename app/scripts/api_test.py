import copy
import requests
import random
import time
import threading

rand_ids = [
    '4989ca86-d33d-4463-9037-eb1d89e29955',
    '4669f3c9-647c-4111-a0c7-7e3d7b5c52a6',
    '2f3b3346-2c4e-47ed-bd3c-db6326c57d3f',
    '549e4112-98ca-4d68-ad39-ba26a78187c4',
    '20fe659d-5f18-4b04-993f-e460bd7ea782',
    '116b03eb-b0bf-4dfd-af9f-1818fadc1153',
    'c870a79d-3b70-432e-a8d8-7be9b989cf7a',
    '2921597c-757b-4ec2-8e78-3f1f7c3020e0',
    '48f1323c-4350-438a-82d4-c16b6808e208',
    '36329a0c-6145-42e9-b2c4-be3e05ab08b5'
]
# List of endpoint URLs to test
endpoints = [
    "http://localhost:8000/user_stats/",
    "http://localhost:8000/city_stats/",
    "http://localhost:8000/parking_stats/",
    "http://localhost:8000/is_parking_available/",
]
endpoints = endpoints + endpoints + endpoints + endpoints + endpoints + endpoints + endpoints + endpoints

# Number of requests to make per endpoint
num_requests = 100

# Dictionary to store the total time for each endpoint
total_time = {endpoint: 0 for endpoint in endpoints}
print(total_time)
# Function to make requests to the API endpoints
def make_requests(endpoint: str):
    s_e = endpoint
    for i in range(num_requests):
        r = endpoint
        if r == "http://localhost:8000/user_stats/":
            r += str(random.randint(1, 99))
        elif r == "http://localhost:8000/city_stats/":
            r += "city" + str(random.randint(1, 99))
        else:
            r += random.choice(rand_ids)

        start_time = time.time()
        response = requests.get(r)
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time[s_e] += elapsed_time
# List to store the threads
threads = []

# Start a thread for each endpoint
for endpoint in endpoints:
    thread = threading.Thread(target=make_requests, args=(endpoint,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

# Calculate the average time for each endpoint
avg_time = {endpoint: total_time[endpoint] / num_requests for endpoint in endpoints}

# Print the results
print("Average time per request:")
for endpoint, time in avg_time.items():
    print(f"{endpoint}: {time:.3f} seconds")