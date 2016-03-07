from .db import session_factory
from .models.twitch import TwitchStream

def get_streams():
    with session_factory() as sess:
        return [x.stream for x in sess.query(TwitchStream.stream).all()]

def get_stream(channel, streamer):
    try:
        with session_factory() as sess:
            return sess.query(TwitchStream).filter(
                TwitchStream.channel==channel,
                TwitchStream.streamer==streamer
            ).one()
    except:
        return None

def list_streams(channel):
    with session_factory() as sess:
        return sess.query(TwitchStream).filter(
            channel==channel
        ).all()

def add_stream(stream):
    try:
        stream = TwitchStream(channel=stream.channel.id, streamer=stream.streamer, stream=stream)
        stream.save()
        return True
    except:
        return False

def delete_stream(channel, streamer):
    try:
        with session_factory() as sess:
            return sess.query(Task).filter(
                TwitchStream.channel==channel,
                TwitchStream.streamer==streamer
            ).delete()
            return True
    except:
        return False
