from .db import session_factory
from .models.twitch import NyaaFeed

def get_feeds():
    with session_factory() as sess:
        return sess.query(NyaaFeed).all()

def get_feed(channel, feed):
    try:
        with session_factory() as sess:
            return sess.query(NyaaFeed).filter(
                NyaaFeed.channel==channel,
                NyaaFeed.url=feed
            ).one()
    except:
        return None

def list_streams(channel):
    with session_factory() as sess:
        return sess.query(NyaaFeed).filter(
            channel==channel
        ).all()

def add_feed(channel, url, json_filter):
    try:
        nyaa = NyaaFeed(channel=channel, url=url, json_filter=json_filter)
        nyaa.save()
        return True
    except:
        return False

def delete_feed(channel, feed):
    try:
        with session_factory() as sess:
            return sess.query(NyaaFeed).filter(
                NyaaFeed.channel==channel,
                NyaaFeed.url==feed
            ).delete()
            return True
    except:
        return False
