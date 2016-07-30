from sqlalchemy import Column, Integer, String

from db.db import Model, session_factory

class NyaaFeed(Model):
    __tablename__ = 'nyaa_feeds'

    id = Column(Integer, primary_key=True)
    channel = Column(Integer)
    url = Column(String)
    json_filter = Column(String)

    def save(self):
        with session_factory() as sess:
            sess.merge(self)

    def delete(self):
        with session_factory() as sess:
            sess.delete(self)
