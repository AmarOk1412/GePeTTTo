#!/usr/bin/env python3

import json
import os
import requests

from gitparser import GitParser

if __name__ == '__main__':
    print('Retrieving projects')
    parser = GitParser(os.getenv('GITLAB_ENDPOINT'), os.getenv('GITLAB_USERS').split(','))
    parser.get_projects()
    for p in parser.projects:
        try:
            print(f'Retrieving issues for project {p['name']} ({p['id']})')
            parser.get_issues_for_training(p['id'], 'rsc/custom.jsonl')
        except Exception as e:
            print(e)
            break