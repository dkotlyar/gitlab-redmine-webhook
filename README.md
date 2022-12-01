# GitLab Redmine Webhook

Create custom field in redmine for store GitLab issue id:
**Admin** -> **Custom fields** -> **New**

1. Format: _Integer_;
2. Use as filter: _True_;

Run in docker:

```shell
docker run -it -p 5000:5000 \
 -e REDMINE_URL=https://redmine.example.com \
 -e REDMINE_KEY=YOUR_API_KEY \
 -e REDMINE_CF_GITLAB_ID=YOUR_CUSTOM_FIELD_ID \
 dkotlyar/gitlab-redmine-webhook
```

If you want to create a comment in Gitlab with Redmine issue link,
pass `GITLAB_URL` and `GITLAB_TOKEN` in environment:

```shell
docker run -it -p 5000:5000 \
 -e REDMINE_URL=https://redmine.example.com \
 -e REDMINE_KEY=YOUR_API_KEY \
 -e REDMINE_CF_GITLAB_ID=YOUR_CUSTOM_FIELD_ID \
 -e GITLAB_URL=https://gitlab.example.com \
 -e GITLAB_TOKEN=YOUR_TOKEN \
 dkotlyar/gitlab-redmine-webhook
```

Other environment variables:

| Variable                      | Notes                                                             |
|-------------------------------|-------------------------------------------------------------------|
| REDMINE_ISSUE_STATUS_INWORK   | Redmine issue status id, when issue in work                       |
| REDMINE_ISSUE_STATUS_DONE     | Redmine issue status id, when issue is done                       |
| GITLAB_ISSUE_STATUS_DONE      | GitLab label title, when issue is done. Default is `Done`         |
| REDMINE_ISSUE_STATUS_DECLINED | Redmine issue status id, when issue is declined                   |
| GITLAB_ISSUE_STATUS_DECLINED  | GitLab label title, when issue is declined. Default is `Declined` |
