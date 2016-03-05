from .db import session_factory
from .models.task import Task

def load():
    with session_factory() as sess:
        return sess.query(Task.task).all()

def add(task):
    task = Task(channel=task.channel.id, name=task.name, task=blob)
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

def list(channel):
    with session_factory() as sess:
        return sess.query(Task.task).filter(
            Task.channel==channel
        ).all()
