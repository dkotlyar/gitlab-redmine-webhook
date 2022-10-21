from os import environ

from flask import Blueprint, request
from redminelib import Redmine

bp = Blueprint('gitlab', __name__)


@bp.route('/<string:project_id>/', methods=['GET', 'POST'])
def hook(project_id):
    redmine_cf_gitlab_id = environ.get("REDMINE_CF_GITLAB_ID")

    gitlab_issue = request.json["object_attributes"]

    redmine = Redmine(url=environ.get('REDMINE_URL'), key=environ.get('REDMINE_KEY'))

    redmine_issue = redmine.issue.filter(
        project_id=project_id,
        **{
            f'cf_{redmine_cf_gitlab_id}': gitlab_issue['iid'],
        }
    )

    if len(redmine_issue):
        redmine_issue = redmine_issue[0]
    else:
        redmine_issue = redmine.issue.new()
        redmine_issue.project_id=project_id

    redmine_issue.save(
        subject=f'GitLab Issue #{gitlab_issue["iid"]}: '
                f'{gitlab_issue["title"]}',
        description=f'{gitlab_issue["description"]}\n\n'
                    f'"GitLab link":{gitlab_issue["url"]}',
        custom_fields=[
            *[
                dict(
                    id=cf.id,
                    value=cf.value
                ) for cf in redmine_issue.custom_fields
                if cf.id != redmine_cf_gitlab_id
            ],
            dict(
                id=redmine_cf_gitlab_id,
                value=gitlab_issue["iid"],
            ),
        ],
    )

    return {}
