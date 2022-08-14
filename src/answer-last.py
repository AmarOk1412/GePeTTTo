#!/usr/bin/env python3

import cmd
import json
import openai
import os

from termcolor import colored, cprint
from gitparser import GitParser


class GePeTTTo(cmd.Cmd):
    prompt = colored('(GePeTTTo) ', 'yellow')
    file = None
    intro = colored('Type help or ? to list commands.\n', 'green')
    parser = GitParser(os.getenv('GITLAB_ENDPOINT'))
    issues = []
    answeringTo = None
    answer = ''

    def answerTo(self, issue):
        '''Answer to an issue via GPT-3 model'''
        # TODO davinci:ft-personal-2022-08-08-02-28-29
        self.answer = openai.Completion.create(\
            model="text-davinci-002",\
            prompt=f"{json.dumps(issue['body'])}",\
            temperature=0, max_tokens=500\
        )['choices'][0]['text']

    def do_help(self, args=''):
        print('start: Start to analyze issues') # DONE
        print('save <file>: save generated answer to <file>')
        print('send: send answer without saving it')
        print('send <file>: send answer from file')
        print('next: pass to the next issue') # DONE
        print('exit: close GePeTTTo') # DONE

    def do_clear(self, arg):
        '''Clear your prompt: CLEAR'''
        os.system('clear')
    
    def do_start(self, arg):
        '''Start the analysis'''
        self.issues = self.parser.get_last_issues()
        self.do_next(arg)
    
    def do_next(self, arg):
        '''Show the next issue to analyze'''
        if self.answeringTo != None:
            # Save last answered issue
            self.parser.set_last_issue(self.answeringTo['id'])
        if len(self.issues) == 0:
            print('No issue to analyze')
            self.do_exit(arg)
        self.answeringTo = self.issues[0]
        self.answerTo(self.answeringTo)
        self.print_issue(self.answeringTo, self.answer)
        self.issues = self.issues[1:]
        print(self.intro)
    
    def do_send(self, arg):
        '''Send answer to GitLab'''
        try:
            if arg != '':
                with open(arg, 'r') as f:
                    self.answer = f.read()
            self.parser.answer(self.answeringTo['id'], self.answeringTo['project'], self.answer)
        except:
            pass
        self.do_next('')
    
    def do_save(self, arg):
        '''Save generated answer to a file'''
        filename = arg if arg != '' else f'{self.answeringTo["id"]}.answer'
        with open(filename, 'w+') as f:
            f.write(self.answer)

    def do_exit(self, arg):
        '''Close GePeTTTo'''
        exit(0)

    def print_issue(self, issue, answer):
        '''Display issue + generated answer'''
        self.do_clear('')
        text = colored(f'Answer to Issue #{issue["id"]} (by {issue["author"]}) - Description:\n', 'green')
        text += colored(issue["body"], 'white')
        text += colored(f'''

====================================================

Proposed answer from GePeTTTo:
''', 'green')
        text += colored(answer, 'white')
        print(text)

 
if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    gepettto = GePeTTTo()
    gepettto.cmdloop()