from os import environ

from redminelib import Redmine


def get_redmine_client():
    return Redmine(url=environ.get('REDMINE_URL'), key=environ.get('REDMINE_KEY'))

