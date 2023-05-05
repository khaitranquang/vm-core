import threading
import traceback

from shared.log.cylog import CyLog


class BackgroundThread:
    def __init__(self, task, interval=1, **kwargs):
        self.task = task
        self.interval = interval

        self.thread = threading.Thread(target=self.task, kwargs=kwargs)
        self.thread.daemon = True
        self.thread.start()
