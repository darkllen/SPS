Rigth db connection creation increase in 10 times

First version: master db only

Worker - 300/s (no difference how many workers are used)

API - queries are sent in different threads (32 threads are used)

http://localhost:8000/user_stats/1: 1.167 seconds
http://localhost:8000/city_stats/city1: 1.665 seconds
http://localhost:8000/parking_stats/fe61be01-6aa0-47ae-a911-44cf88f4b284: 1.532 seconds
http://localhost:8000/is_parking_available/fe61be01-6aa0-47ae-a911-44cf88f4b284: 0.930 seconds

Using togeter make worker unstable, process one time in second


ro replica (bitnami image, right flow): 

Worker - 40/s 


pub/sub replica: 

Worker - 400/s (no difference how many workers are used)

API - queries are sent in different threads (32 threads are used)

http://localhost:8000/user_stats/: 1.937 seconds
http://localhost:8000/city_stats/: 2.206 seconds
http://localhost:8000/parking_stats/: 2.099 seconds
http://localhost:8000/is_parking_available/: 1.677 seconds

Using togeter not make worker unstable, process one time in second
