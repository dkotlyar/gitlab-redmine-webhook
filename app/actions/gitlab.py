from os import environ

from gitlab import Gitlab


def get_gitlab_client():
    if token := environ.get('GITLAB_TOKEN'):
        return Gitlab(url=environ.get('GITLAB_URL'), private_token=token)
