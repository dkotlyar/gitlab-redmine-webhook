import traceback
from os import environ

from flask import Blueprint, request
from none_aware import Maybe

from app.actions.gitlab import get_gitlab_client
from app.actions.redmine import get_redmine_client

bp = Blueprint('gitlab', __name__)


@bp.route('/<string:project_id>/', methods=['GET', 'POST'])
def hook(project_id):
    data = Maybe(request.json)
    gitlab_issue = data.object_attributes

    redmine_cf_id = environ.get('REDMINE_CF_GITLAB_ID')
    redmine_issue_status_inwork = int(environ.get('REDMINE_ISSUE_STATUS_INWORK'))
    redmine_issue_status_done = int(environ.get('REDMINE_ISSUE_STATUS_DONE'))
    gitlab_issue_status_done = environ.get('GITLAB_ISSUE_STATUS_DONE', 'Done')
    redmine_issue_status_declined = int(environ.get('REDMINE_ISSUE_STATUS_DECLINED'))
    gitlab_issue_status_declined = environ.get('GITLAB_ISSUE_STATUS_DECLINED', 'Declined')

    redmine = get_redmine_client()
    gitlab = get_gitlab_client()

    redmine_issue = redmine.issue.filter(
        project_id=project_id,
        **{
            f'cf_{redmine_cf_id}': gitlab_issue.id.else_(0),
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
        value=gitlab_issue.id.else_(0),
    ))

    try:
        if gitlab_issue.assignee_id():
            assignee_username = [
                Maybe(user).username.else_('')
                for user in data.assignees.else_([])
                if Maybe(user).id() == gitlab_issue.assignee_id()
            ]
            if assignee_username:
                assignee_username = assignee_username[0]
                assignee_ids = [
                    user.id
                    for membership in redmine.project_membership.filter(project_id=project_id)
                    if (user := redmine.user.get(Maybe(membership).user.id())).login == assignee_username
                ]
                if assignee_ids:
                    redmine_issue.assigned_to_id = assignee_ids[0]
            redmine_issue.status_id = redmine_issue_status_inwork
        else:
            redmine_issue.assigned_to_id = None
    except:
        pass

    if any(label['title'] == gitlab_issue_status_done for label in gitlab_issue.labels.else_([])):
        redmine_issue.status_id = redmine_issue_status_done
        redmine_issue.done_ratio = 100

    if any(label['title'] == gitlab_issue_status_declined for label in gitlab_issue.labels.else_([])):
        redmine_issue.status_id = redmine_issue_status_declined
        redmine_issue.done_ratio = 0

    redmine_issue.save(
        subject=f'GitLab Issue #{gitlab_issue.iid.else_(0)}: '
                f'{gitlab_issue.title.else_("")}',
        description=f'{gitlab_issue.description.else_("")}\n\n'
                    f'"GitLab link":{gitlab_issue.url.else_("")}',
        custom_fields=custom_fields,
    )

    if gitlab and create_notes:
        gl_issue = (
            gitlab
            .projects.get(data.project.id.else_(''))
            .issues.get(gitlab_issue.iid.else_(0))
        )

        gl_issue.notes.create(dict(
            body=f'[Redmine issue #{redmine_issue.id}]({redmine.url}/issues/{redmine_issue.id})',
        ))

    return {}
