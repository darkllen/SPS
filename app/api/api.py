from fastapi import FastAPI
from db.connection import get_session
from db.database import Event, Sensor
from sqlalchemy import select, text, func
from sqlalchemy import Float
from sqlalchemy.orm import aliased
from uuid import UUID
from enitites.sensor_event import EventStatus
from cache.redis_imp import redis 
import json


app = FastAPI()

#time user is used parking
#count times user used parking
@app.get("/user_stats/{id}")
async def user_stats(id: int):
    if r:=redis.get(f'u{id}'):
        return {"usage_parking_time":r}
    async with get_session() as session:

        query = select(func.sum(Event.data.op('->')('in_usage_s').cast(Float))).filter(
            Event.data.op("@>")({"user_id":id})
        )
        raw = await session.execute(query)
        raw = raw.fetchone()
        redis.set(f'u{id}', raw[0], ex=60)
        return {"usage_parking_time":raw[0]}

#time parking was available
#time parking was used
@app.get("/city_stats/{city}")
async def city_stats(city: str):
    if r:=redis.get(f'c{city}'):
        return json.loads(r)
    async with get_session() as session:
        a1 = aliased(Sensor)
        query = select(func.sum(Event.data.op('->')('in_usage_s').cast(Float)), func.sum(Event.data.op('->')('available_s').cast(Float))).join(a1, Event.sensor).filter(
            a1.city == city
        )
        raw = await session.execute(query)
        raw = raw.fetchone()
        res = {"summary_parking_time":raw[0], "summary_available_time":raw[1]}
        redis.set(f'c{city}', json.dumps(res), ex=60)
        return res
    
#time parking was available
#time parking was used
@app.get("/parking_stats/{external_id}")
async def parking_stats(external_id: UUID):
    if r:=redis.get(f'ps{str(external_id)}'):
        return json.loads(r)
    async with get_session() as session:
        query = select(func.sum(Event.data.op('->')('in_usage_s').cast(Float)), func.sum(Event.data.op('->')('available_s').cast(Float))).filter(
            Event.sensor_external_id == str(external_id)
        )
        raw = await session.execute(query)
        raw = raw.fetchone()
        res = {"summary_parking_time":raw[0], "summary_available_time":raw[1]}
        redis.set(f'ps{str(external_id)}', json.dumps(res), ex=60)
        return res
    
@app.get("/is_parking_available/{external_id}")
async def is_parking_available(external_id: UUID):
    if r:=redis.get(f'pa{str(external_id)}'):
        return r == EventStatus.AVAILABLE
    async with get_session() as session:
        query = select(Sensor.status).filter(
            Sensor.external_id == str(external_id)
        )
        raw = await session.execute(query)
        raw = raw.fetchone()
        redis.set(f'pa{str(external_id)}', raw[0], ex=60)
        return raw[0] == EventStatus.AVAILABLE