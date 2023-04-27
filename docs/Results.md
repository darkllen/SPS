### Technical solutions used:
* docker-compose
* rabbtimq
* postgres
* alembic
* fastapi
* nginx
* redis


### Initial upgrades:
    Rigth db connection creation and async increase results in 10 times

### Test scenarios:

##### Worker
emulate random messages from devices to the queue async in 64 threads

##### API
make queries to endpoints with random data and measure responce time (32 threads)


### First version: master db only

##### Worker
* Throughput - 300/s
* No difference how many workers are used
##### API
* no difference how many pods are used
* average responce time:
    * user_stats: 1.167 seconds
    * city_stats: 1.665 seconds
    * parking_stats: 1.532 seconds
    * is_parking_available: 0.930 seconds
* using togeter with workers make worker unstable cause of selects, slow them down
##### Note
default realisation, no interesting things


### Second version: master+slave (bad experience)

##### Worker
* Throughput - 40/s 
##### API
* Unknown, wasn't tested
##### Note
bitnami image was used for auto replication, very slow by some reason

### Third version: master+slave (from lab)

##### Worker
* Throughput - 400/s
##### API
* average responce time:
    * user_stats: 1.937 seconds
    * city_stats: 2.206 seconds
    * parking_stats: 2.099 seconds
    * is_parking_available: 1.051 seconds
* using togeter with workers make worker unstable, process one time in second, slow it down
##### Note
workers became faster, api slower
was used replication from the lab based on pub/sub

### Fourth version: add redis for workers and api

##### Worker
* Throughput - 600/s
##### API
* average responce time from the start:
    * user_stats: 0.767 seconds
    * city_stats: 0.787 seconds
    * parking_stats: 0.624 seconds
    * is_parking_available: 0.589 seconds
* average responce time after some time:
    * user_stats: 0.482 seconds
    * city_stats: 0.482 seconds
    * parking_stats: 0.478 seconds
    * is_parking_available: 0.475 seconds
##### Note
fast worker, fast api, but
using api with workers at the same time leads to worker Throughput around 60/s, that is really slow

### Final version: add redis for api only

##### Worker
* Throughput - 400/s
##### API
* average responce time from the start:
    * user_stats: 0.482 seconds
    * city_stats: 0.482 seconds
    * parking_stats: 0.478 seconds
    * is_parking_available: 0.475 seconds
##### Note
combine worker throughput from third variant and api responce time from the fourth