import sys
import os
import requests
import json

issue_link = "https://nyss.pro/helpdesk/issue/"


def find_issue(task_code):
    with open('cache.json', 'r', encoding='utf-8') as f:
        tasks = json.loads(f.read())
        for task in tasks:
            exerciseShortName = task.get('exerciseShortName')
            if exerciseShortName == task_code:
                print(f"id:{task['id']}. link: {issue_link + str(task['id'])}")


def get_issues(token):
    url = "https://nyss.pro/report/issuelist?page=0&pageSize=10000&filter="
    header = f"Bearer {token}"
    data = requests.get(url=url, headers={"Authorization": header})
    return data.json()


def cache_issues():
    token = os.environ.get("NYSS_TOKEN", None)
    if not token:
        print(f"wrong token: {token}")
        return 1
    issues = get_issues(token)
    with open('cache.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(issues))


def main(argv):
    if len(argv) < 1:
        print('incorrect arguments number')
        return 0
    task = argv[0]
    if 'refresh' in argv:
        cache_issues()
    find_issue(task)


if __name__ == '__main__':
    argv = sys.argv[1:]
    main(argv)
