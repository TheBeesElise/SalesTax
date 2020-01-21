from os import environ

from django import setup


def start_session():
    environ.setdefault('DJANGO_SETTINGS_MODULE', "orm.settings")
    setup()