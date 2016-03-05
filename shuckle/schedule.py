import pickle

from .db import session_factory
from .models.task import Task

def load():
    with session_factory() as sess:
        return sess.query(Task.task).all()

def add(task):
    blob = pickle.dumps(task, pickle.HIGHEST_PROTOCOL)
    task = Task(task.channel.id, task.name, blob)
    task.save()

def delete(channel, name):
    with session_factory() as sess:
        try:
            query = sess.query(Task).filter(
                Task.channel==channel,
                Task.name==name
            ).delete()

            return True
        except:
            return False

def list():
    with session_factory() as sess:
        tasks = sess.query(Task).all()
        ret = [pickle.loads(x.task) for x in tasks]
