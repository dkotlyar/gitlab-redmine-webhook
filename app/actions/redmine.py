from os import environ

from none_aware import Maybe
from redminelib import Redmine


def get_redmine_client():
    return Redmine(url=environ.get('REDMINE_URL'), key=environ.get('REDMINE_KEY'))


def get_project_users(redmine, project_id):
    members = []
    for membership in redmine.project_membership.filter(project_id=project_id):
        try:
            members.append(redmine.user.get(Maybe(membership).user.id()))
        except:
            pass
    return members
