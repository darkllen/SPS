from fastapi import FastAPI
from db.connection import get_session
from db.database import Event, Sensor
from sqlalchemy import select, text, func
from sqlalchemy import Float
from sqlalchemy.orm import aliased
from uuid import UUID
from enitites.sensor_event import EventStatus


app = FastAPI()

#time user is used parking
#count times user used parking
@app.get("/user_stats/{id}")
async def user_stats(id: int):
    async with get_session() as session:
        query = select(func.sum(Event.data.op('->')('in_usage_s').cast(Float))).filter(
            Event.data.op("@>")({"user_id":id})
        )
        raw = await session.execute(query)
        raw = raw.fetchone()
        return {"usage_parking_time":raw[0]}

#time parking was available
#time parking was used
@app.get("/city_stats/{city}")
async def city_stats(city: str):
    async with get_session() as session:
        a1 = aliased(Sensor)
        query = select(func.sum(Event.data.op('->')('in_usage_s').cast(Float)), func.sum(Event.data.op('->')('available_s').cast(Float))).join(a1, Event.sensor).filter(
            a1.city == city
        )
        raw = await session.execute(query)
        raw = raw.fetchone()
        return {"summary_parking_time":raw[0], "summary_available_time":raw[1]}
    
#time parking was available
#time parking was used
@app.get("/parking_stats/{external_id}")
async def parking_stats(external_id: UUID):
    async with get_session() as session:
        query = select(func.sum(Event.data.op('->')('in_usage_s').cast(Float)), func.sum(Event.data.op('->')('available_s').cast(Float))).filter(
            Event.sensor_external_id == str(external_id)
        )
        raw = await session.execute(query)
        raw = raw.fetchone()
        return {"summary_parking_time":raw[0], "summary_available_time":raw[1]}
    
@app.get("/is_parking_available/{external_id}")
async def is_parking_available(external_id: UUID):
    async with get_session() as session:
        query = select(Sensor).filter(
            Sensor.external_id == str(external_id)
        )
        raw = await session.execute(query)
        raw = raw.fetchone()
        return raw[0] == EventStatus.AVAILABLE