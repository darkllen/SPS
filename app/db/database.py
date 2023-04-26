# from sqlalchemy import create_engine
# from sqlalchemy import MetaData
# import pymysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy import create_engine, Column, Integer, String, Enum, DateTime, text, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.sql import text
from datetime import datetime
from sqlalchemy.orm import declarative_base, relationship, Mapped

Base = declarative_base()

# Define the possible status values for the enum column
SENSOR_STATUS_ENUM = Enum('available', 'in_usage', name='sensor_status_enum')
EVENT_NAME_ENUM = Enum('locked', 'unlocked', name='event_name_enum')

class Sensor(Base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String(255), nullable=False, unique=True)
    city = Column(String(255), nullable=False)
    status = Column(SENSOR_STATUS_ENUM, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('(now())'))
    updated_at = Column(DateTime, nullable=False, onupdate=datetime.utcnow, server_default=text('(now())'))

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_external_id = Column(String(255), ForeignKey("sensors.external_id"), nullable=False)
    event_name = Column(EVENT_NAME_ENUM, nullable=False)
    created_at = Column(DateTime, nullable=False, default=text('(now())'))
    data = Column(JSONB, nullable=False)
    sensor: Mapped["Sensor"] = relationship()

    __table_args__ = (Index('ix_data_gin', data, postgresql_using="gin"), )


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('(now())'))
