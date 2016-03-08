from sqlalchemy import Column, Integer, String

from db.db import Model, session_factory

class ModuleStatus(Model):
    __tablename__ = 'module_status'

    id = Column(Integer, primary_key=True)
    channel = Column(Integer)
    module = Column(String)
    status = Column(Integer)

    def save(self):
        with session_factory() as sess:
            sess.merge(self)

    def delete(self):
        with session_factory() as sess:
            sess.delete(self)
