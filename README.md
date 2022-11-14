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
