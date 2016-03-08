from sqlalchemy import Column, Integer, PickleType, String

from db.db import Model, session_factory

class Task(Model):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    channel = Column(Integer)
    name = Column(String)
    task = Column(PickleType)

    def save(self):
        with session_factory() as sess:
            sess.merge(self)

    def delete(self):
        with session_factory() as sess:
            sess.delete(self)
