"""
Description
===========

Usage
=====

.. code-block:: python

  #!/usr/bin/env python3

  from flask import Flask
  from flask_gordon.ext import CeleryExt

  flask = Flask(__name__)
  celery = CeleryExt(flask)


Classes
=======

.. autoclass:: Celery
   :members: init_app

"""
import typing as t

try:
    from celery import Celery, Task

    HAS_CELERY = True
except ImportError:
    HAS_CELERY = False


DEFAULT_CONFIGURATION = {
    "broker_url": "redis://localhost:6379/0",
    "result_backend": "redis://localhost:6379/0",
    "broker_connection_retry_on_startup": False,
}


class CeleryExt:
    def __init__(self):
        if not HAS_CELERY:
            raise NotImplementedError("CeleryExt requires celery[redis] package")

    def init_app(
        self,
        app: "Flask",
        configuration=None,
    ):
        """
        Parameters
        ----------
        app: FlaskApp

            A Flask application.

        configuration: dict

            If a configuration dictionnary is passed, it will be used.
            Otherwise, a configuration will be searched for in app.config["CELERY"].

        """

        # pylint: disable=abstract-method
        class FlaskTask(Task):
            def __call__(self, *args: object, **kwargs: t.Dict[str, t.Any]) -> object:
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery_app = Celery(app.name, task_cls=FlaskTask)

        # Set the first configuration that we find
        if not configuration:
            for name in ["celery", "CELERY"]:
                if name in app.config:
                    configuration = app.config[name]
                    break

        # Defaults
        # cf: https://docs.celeryq.dev/en/stable/userguide/configuration.html#example-configuration-file
        configuration = configuration or {}
        configuration = {**DEFAULT_CONFIGURATION, **configuration}

        app.config["CELERY"] = configuration
        celery_app.config_from_object(configuration)

        celery_app.set_default()
        app.extensions["celery"] = celery_app

        return celery_app
