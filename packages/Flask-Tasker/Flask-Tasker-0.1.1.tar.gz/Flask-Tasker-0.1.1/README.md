Flask-Tasker
==============

Simplify task management in flask applications.

Installation
------------

You can install this package as usual with pip:

    pip install flask-tasker

Example
-------

```py
import time

from flask import Flask
from flask_socketio import SocketIO
from flask_tasker import FlaskTasker

app = Flask(__name__)
socketio = SocketIO(app)
flask_tasker = FlaskTasker(app, socketio)

flags = {}

@flask_tasker.dispose()
def dispose(task_id, on_progress, on_success, on_error):
    flags[task_id] = False

    # Simulate task progress.
    count = 5
    for i in range(count):
        if flags[task_id]:
            return
        time.sleep(1)
        on_progress(data={'progress': (i + 1) / count * 100})

    # Simulate task success or failure.
    if (round(time.time()) % 2 == 0):
        on_success()
    else:
        on_error()


@flask_tasker.terminate()
def terminate(task_id):
    flags[task_id] = True


if __name__ == '__main__':
    flask_tasker.run()
```

Resources
---------

- [Github](https://github.com/xuhuanstudio/flask-tasker)
- [PyPI](https://pypi.python.org/pypi/Flask-Tasker)
