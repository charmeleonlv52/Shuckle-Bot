from sqlalchemy import Column, Integer, String

from .generic import GenericModel

class ModuleStatus(GenericModel):
    __tablename__ = 'module_status'

    id = Column(Integer, primary_key=True)
    channel = Column(Integer)
    module = Column(String)
    status = Column(Integer)
