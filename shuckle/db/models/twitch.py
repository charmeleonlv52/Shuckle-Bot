from sqlalchemy import Column, Integer, PickleType, String

from db.db import Model, session_factory

class TwitchStream(Model):
    __tablename__ = 'twitch_streams'

    id = Column(Integer, primary_key=True)
    channel = Column(Integer)
    streamer = Column(String)
    stream = Column(PickleType)

    def save(self):
        with session_factory() as sess:
            sess.merge(self)

    def delete(self):
        with session_factory() as sess:
            sess.delete(self)
