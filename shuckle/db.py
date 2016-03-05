import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from contextlib import contextmanager

from config import config

eng = 'sqlite:////{}'.format(os.path.join(config.__DATA__, 'shuckle.db'))
engine = create_engine(eng)
factory = sessionmaker(bind=engine)
Session = scoped_session(factory)
Model = declarative_base()

@contextmanager
def session_factory():
	s = Session()

	try:
		yield s
		s.commit()
	except:
		s.rollback()
		raise
	finally:
		s.close()
