#!/usr/bin/env python3

import json
import os
import requests

class GitParser:
    """GitParser uses GitLab's API to parse issues"""
    def __init__(self, url, users_wanted = [], ignore_in = [], ignore_start = []):
        self.git_url = url
        self.projects = []
        self.users_wanted = users_wanted
        self.headers = {'PRIVATE-TOKEN': os.getenv('GITLAB_API_KEY')}
        self.ignore_in = ['/uploads/', '```'] if len(ignore_in) == 0 else ignore_in
        self.ignore_start = ['mentioned in', 'moved', 'assigned to', 'added to epic', \
                             'changed the description', 'changed title from', \
                             'unassigned', 'closed', 'reopened', 'added ', 'removed ', \
                             'changed milestone to'] if len(ignore_start) == 0 else ignore_start

    def get_projects(self):
        """Retrieve all projects from a gitlab instance"""
        endpoint = f'{self.git_url}/api/v4/projects'
        resp = requests.get(endpoint)
        data = resp.json()
        for obj in data:
            self.projects.append({
                'id': obj['id'],
                'name': obj['name'],
            })

    def get_issues_for_training(self, project_id, training_file):
        """Write in training_file comment from wanted users for customizing a GPT-3 model.
           This parts gets issues, get_discussion the following comments"""
        p = 0
        with open(file, 'a+') as training_file:
            while True:
                endpoint = f'{self.git_url}/api/v4/projects/{project_id}/issues?per_page=50&page={p}'
                resp = requests.get(endpoint)
                data = resp.json()
                for obj in data:
                    try:
                        comment = {'author': obj['author']['id'], 'body': f'{obj["title"]}\n\n{obj["description"]}'}
                        issue = {'id': obj['iid'], 'discussion': [comment]}
                        self.get_discussion(id, issue, training_file)
                    except Exception as e:
                        print(f'Failed to get issues: {e}')
                        return
                p += 1
                if len(data) != 50:
                    break
            
    def get_discussion(self, project_id, issue, training_file):
        """cf get_issues_for_training"""
        endpoint = f'{self.git_url}/api/v4/projects/{project_id}/issues/{issue["id"]}/discussions?per_page=50'
        print(f'Retrieving discussion for project {p["name"]} (#{issue["id"]})')
        resp = requests.get(url=endpoint, headers = self.headers)
        data = resp.json()
        for obj in data:
            try:
                note = obj['notes'][0]
                author = note['author']['id']
                body = note['body']
                if any(body.find(x) != -1 for x in self.ignore_in) or any(body.find(x) != 0 for x in self.ignore_start):
                    continue
                if len(self.users_wanted) == 0 or author in self.users_wanted:
                    lastBody = "Answer to this issue:\\n\\n" + issue['discussion'][-1]['body']
                    body = body + "###"
                    d = "{" + f'"prompt": {json.dumps(lastBody)}, "completion": {json.dumps(body)}' + "}\n"
                    print(d)
                    training_file.write(d)
                issue['discussion'].append({ 'author': author, 'body': body})
            except Exception as e:
                print(f'Failed to get discussion: {e}')
                return

    
    def get_last_issues(self):
        """Retrieve last issue's ids, author, and body (read/write a file named lastIssue)"""
        lastIssue = 0
        try:
            with open('lastIssue', 'r') as lastIssueFile:
                lastIssue = lastIssueFile.read().strip()
        except Exception as e:
            print(f'Error while retrieving last issue: {e}')

        lastIssues = []
        p = 0
        while True:
            try:
                endpoint = f'{self.git_url}/api/v4/issues?scope=all&per_page=50&page={p}'
                resp = requests.get(url=endpoint, headers=self.headers)
                data = resp.json()
                if p == 0:
                    firstIssue = data[0]['iid']
                for obj in data:
                    iid = obj['iid']
                    if lastIssue == str(iid):
                        return lastIssues
                    lastIssues.append({'id': iid, \
                                       'project': obj['project_id'], \
                                       'author': obj['author']['username'], \
                                       'body': f'{obj["title"]}\n\n{obj["description"]}'})
                p += 1
                if len(data) != 50:
                    break
            except Exception as e:
                print(f'Error while retrieving issues: {e}')
                break
        return lastIssues
    
    def set_last_issue(self, issue):
        with open('lastIssue', 'w') as lastIssueFile:
            print(f'Save last issue: {issue}')
            lastIssueFile.write(str(issue))
    
    def answer(self, project_id, issue_id, body):
        """Answer to an issue on the specified issue"""
        endpoint = f'{self.git_url}/api/v4/projects/{project_id}/issues/{issue_id}/notes?body={body}'
        response = requests.post(endpoint, headers=self.headers)
        if 'error' in response.json():
            print(f'An error occurred while posting to {endpoint}')
        else:
            print(f'Answered to issue {issue_id} with success')