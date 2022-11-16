from os import environ

from flask import Blueprint, request

from app.actions.gitlab import get_gitlab_client
from app.actions.redmine import get_redmine_client

bp = Blueprint('gitlab', __name__)


@bp.route('/<string:project_id>/', methods=['GET', 'POST'])
def hook(project_id):
    data = request.json
    gitlab_issue = data['object_attributes']

    redmine_cf_id = environ.get('REDMINE_CF_GITLAB_ID')

    redmine = get_redmine_client()
    gitlab = get_gitlab_client()

    redmine_issue = redmine.issue.filter(
        project_id=project_id,
        **{
            f'cf_{redmine_cf_id}': gitlab_issue['id'],
        }
    )

    create_notes = False
    if len(redmine_issue):
        redmine_issue = redmine_issue[0]
    else:
        redmine_issue = redmine.issue.new()
        redmine_issue.project_id = project_id
        create_notes = True

    custom_fields = [
        dict(id=cf['id'], value=cf['value'])
        for cf in redmine_issue.custom_fields
        if cf['id'] != redmine_cf_id
    ]
    custom_fields.append(dict(
        id=redmine_cf_id,
        value=gitlab_issue['id'],
    ))

    redmine_issue.save(
        subject=f'GitLab Issue #{gitlab_issue["iid"]}: '
                f'{gitlab_issue["title"]}',
        description=f'{gitlab_issue["description"]}\n\n'
                    f'"GitLab link":{gitlab_issue["url"]}',
        custom_fields=custom_fields,
    )

    if gitlab and create_notes:
        gl_issue = (
            gitlab
            .projects.get(data['project']['id'])
            .issues.get(gitlab_issue['iid'])
        )

        gl_issue.notes.create(dict(
            body=f'[Redmine issue #{redmine_issue.id}]({redmine.url}/issues/{redmine_issue.id})',
        ))

    return {}
