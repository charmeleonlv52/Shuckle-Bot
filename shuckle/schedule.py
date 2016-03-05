from .db import session_factory
from .models.task import Task

def load_schedule():
    with session_factory() as sess:
        return [x.task for x in sess.query(Task.task).all()]

def add_task(task):
    try:
        task = Task(channel=task.channel.id, name=task.name, task=blob)
        task.save()
        return True
    except:
        return False

def get_task(channel, name):
    try:
        with session_factory() as sess:
            return sess.query(Task).filter(
                Task.channel==channel,
                Task.name==name
            ).one()
    except:
        return None

def delete_task(channel, name):
    try:
        with session_factory() as sess:
            query = sess.query(Task).filter(
                Task.channel==channel,
                Task.name==name
            ).delete()

            return True
    except:
        return False

def list_tasks(channel):
    with session_factory() as sess:
        return sess.query(Task.task).filter(
            Task.channel==channel
        ).all()
