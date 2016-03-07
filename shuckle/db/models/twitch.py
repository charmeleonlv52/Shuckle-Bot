from sqlalchemy import Column, Integer, PickleType, String

from .generic import GenericModel

class TwitchStream(GenericModel):
    __tablename__ = 'twitch_streams'

    id = Column(Integer, primary_key=True)
    channel = Column(Integer)
    streamer = Column(String)
    stream = Column(Pickle)
