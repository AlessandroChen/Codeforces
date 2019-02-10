#!/usr/bin/python3

from urllib.request import urlopen
from bs4 import BeautifulSoup

from sys import argv
from subprocess import call

import re
import os

# Generates the test script.

SAMPLE_INPUT='input'
SAMPLE_OUTPUT='output'
MY_OUTPUT='my_output'

Header = "https://codeforc.es/"
#Header = "https://codeforces.com/"

RED_F='\033[31m'
GREEN_F='\033[32m'
BOLD='\033[1m'
NORM='\033[0m'
TIME_CMD='`which time` -o time.out -f "(%es)"'
TIME_AP='`cat time.out`'

def generate_test_script(folder, num_tests, problem, contest):
    param = {
            'TEMPLATE'    : 'template.cpp',
            'DEBUG_FLAGS' : '-DDEBUG',
            'COMPILE_CMD' : 'g++ -g -std=c++11 -Wall $DBG',
            'RUN_CMD'     : './a.out'
        }

    with open(folder + 'test.sh', 'w') as test:
        test.write(
            ('#!/bin/bash\n'
            'DBG=""\n'
            'while getopts ":d" opt; do\n'
            '  case $opt in\n'
            '    d)\n'
            '      echo "-d was selected; compiling in DEBUG mode!" >&2\n'
            '      DBG=' + param["DEBUG_FLAGS"] +'\n'
            '      ;;\n'
            '    \?)\n'
            '      echo "Invalid option: -$OPTARG" >&2\n'
            '      ;;\n'
            '  esac\n'
            'done\n'
            '\n'
            'if ! ' + param["COMPILE_CMD"] +' {0}.{1}; then\n'
            '    exit\n'
            'fi\n'
            'INPUT_NAME='+SAMPLE_INPUT+'\n'
            'OUTPUT_NAME='+SAMPLE_OUTPUT+'\n'
            'MY_NAME='+MY_OUTPUT+'\n'
            'rm -R $MY_NAME* &>/dev/null\n').format(problem, param["TEMPLATE"].split('.')[1]))
        test.write(
            'for test_file in $INPUT_NAME*\n'
            'do\n'
            '    i=$((${{#INPUT_NAME}}))\n'
            '    test_case=${{test_file:$i}}\n'
            '    if ! {5} {run_cmd} < $INPUT_NAME$test_case > $MY_NAME$test_case; then\n'
            '        echo {1}{4}Sample test \#$test_case: Runtime Error{2} {6}\n'
            '        echo ========================================\n'
            '        echo Sample Input \#$test_case\n'
            '        cat $INPUT_NAME$test_case\n'
            '    else\n'
            '        if diff --brief --ignore-space-change $MY_NAME$test_case $OUTPUT_NAME$test_case; then    \n'
            '            echo {1}{3}Sample test \#$test_case: Accepted{2} {6}\n'
            '        else\n'
            '            echo {1}{4}Sample test \#$test_case: Wrong Answer{2} {6}\n'
            '            echo ========================================\n'
            '            echo Sample Input \#$test_case\n'
            '            cat $INPUT_NAME$test_case\n'
            '            echo ========================================\n'
            '            echo Sample Output \#$test_case\n'
            '            cat $OUTPUT_NAME$test_case\n'
            '            echo ========================================\n'
            '            echo My Output \#$test_case\n'
            '            cat $MY_NAME$test_case\n'
            '            echo ========================================\n'
            '        fi\n'
            '    fi\n'
            'done\n'
            .format(num_tests, BOLD, NORM, GREEN_F, RED_F, TIME_CMD, TIME_AP, run_cmd=param["RUN_CMD"]))
    call(['chmod', '+x', folder + 'test.sh'])

    with open(folder + 'submit.sh', 'w') as submit:
            submit.write('#!/bin/bash\n')
            submit.write('idne ' + contest + problem + ' ' + problem + '.cpp \n')
    call(['chmod', '+x', folder + 'submit.sh'])


class CodeforcesContestParse:

    def ParseContestPage(self, contest):
        self.html = urlopen(Header + "contest/" + contest);
        bsObj = BeautifulSoup(self.html, features="html.parser");
        self.contest_name = bsObj.table.find("a").get_text();

        print (("*** Round Name: \033[4m%s\033[0m ***" % self.contest_name));

        self.contest_list = [];
        self.contest_links = [];
        self.contest_names = [];

        for name in bsObj.findAll("td", {"class": "id"}):
            t_name = name.get_text();
            contest_name = t_name.replace("\n", "");
            self.contest_list.append(contest_name.strip());

        os.mkdir(contest);

        t_Links = bsObj.find('table', {"class":"problems"}).findAll('a', {"href":re.compile("\/contest/[a-z0-9]*\/problem\/[a-zA-Z0-9]")});

        for link in t_Links[0::2]:
            self.contest_links.append(link['href']);

        print ("Found %d problems!" % len(self.contest_links));

        for link in bsObj.findAll("div", {"style": "float: left;"}):
            self.contest_names.append(link.get_text().strip());

    def getLinks():
        return self.contest_links;

    def ParseProblemPage(self, Link, contest, problem):
        numList = ["1", "2", "3", "4", "5", "6", "7", "8", "9"];
        html = urlopen(Link);
        Dir = './' + contest + '/' + problem + '/';
        os.mkdir(Dir[:-1]);
        bsOBJ = BeautifulSoup(html, features="html.parser");
        i = 0;
        for name in bsOBJ.find_all("div", {"class":"input"}):
            input_file = open(Dir + "input" + numList[i], 'w')
            t_text = name.get_text()
            text = t_text[5:].strip();
            input_file.write(text)
            i = i + 1

        generate_test_script(Dir, i, problem, contest);
        print ("%d sample test(s) found" % i);
        print ("="*40)

        i = 0;
        for name in bsOBJ.find_all("div", {"class":"output"}):
            input_file = open(Dir + "output" + numList[i], 'w')
            t_text = name.get_text()
            text = t_text[6:].strip();
            input_file.write(text)
            i = i + 1

    def Process(self, contest):
        for i in range(0, len(self.contest_links)):
            Link = self.contest_links[i]; ID = self.contest_list[i]; Name = self.contest_names[i];
            print("Downloading Problem {0} : {0} - {1}".format(ID, Name));
            self.ParseProblemPage(Header + Link, contest, ID);


def main():
    print ("Please Enter the Contest ID:");
    contest = input(">> ");
    Contest = CodeforcesContestParse();
    Contest.ParseContestPage(contest);
    Contest.Process(contest);
    print ('Use ./test.sh to run sample tests in each directory.')
    print ('Use ./submit.sh to submit code.')

if __name__ == '__main__':
    main()
