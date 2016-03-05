from .db import session_factory
from .models.status import ModuleStatus

def is_enabled(module, channel):
    with session_factory() as sess:
        try:
            query = sess.query(ModuleStatus.status).filter(
                ModuleStatus.channel==channel,
                ModuleStatus.module==module
            ).one()

            return query.status != 0
        except:
            return True

def enable_module(module, channel):
    try:
        with session_factory() as sess:
            status = sess.query(ModuleStatus).filter(
                ModuleStatus.channel==channel,
                ModuleStatus.module==module
            )

            if not status:
                status = ModuleStatus(channel=channel, module=module)

            status.status = True
            status.save()
            return True
    except:
        return False

def disable_module(module, channel):
    try:
        with session_factory() as sess:
            status = sess.query(ModuleStatus).filter(
                ModuleStatus.channel==channel,
                ModuleStatus.module==module
            ).first()

            if not status:
                status = ModuleStatus(channel=channel, module=module)

            status.status = False
            status.save()
            return True
    except:
        return False
