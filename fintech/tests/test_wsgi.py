import os

from django.core.handlers.wsgi import WSGIHandler
from fintech.wsgi import application


def test_wsgi_default_settings():
    assert 'fintech.settings' == os.environ["DJANGO_SETTINGS_MODULE"]


def test_application_instace():
    assert isinstance(application, WSGIHandler)
