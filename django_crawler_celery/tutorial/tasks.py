import time

import requests
from celery import shared_task, chain, uuid
from django.conf import settings

from .utils import create_csv


def chain_tasks(language):
    # crawler_repos ->  build_report_task
    task_id = uuid()
    chain(crawler_repos.s(language, 1000, 1), build_report_task.subtask(args=(task_id,), task_id=task_id))()
    return task_id


'''
ref. http://docs.celeryq.org/en/latest/userguide/tasks.html#ignore-results-you-don-t-want
'''


@shared_task(ignore_result=True)
def crawler_repos(language, per_page, page):
    payload = {
        'sort': 'stars',
        'order': 'desc',
        'q': 'language:{}'.format(language),
        'per_page': per_page,
        'page': page
    }
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': 'token {}'.format(settings.GITHUB_OAUTH)
    }
    r = requests.get(
        'https://api.github.com/search/repositories',
        params=payload,
        headers=headers)

    # Simulation file conversion
    time.sleep(10)

    items = r.json()['items']
    return items


@shared_task(ignore_result=False)
def build_report_task(results, task_id):
    rows = [
        [repo.get('name'), repo.get('full_name'), repo.get('html_url'), repo.get('description')]
        for repo in results
    ]
    filename = '{}/github-repos-{}.csv'.format(settings.MEDIA_ROOT, task_id)

    # Simulation file conversion
    time.sleep(10)

    return create_csv(filename, rows)
