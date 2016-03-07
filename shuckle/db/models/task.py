from sqlalchemy import Column, Integer, PickleType, String

from .generic import GenericModel

class Task(GenericModel):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    channel = Column(Integer)
    name = Column(String)
    task = Column(PickleType)
