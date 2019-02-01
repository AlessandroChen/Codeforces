from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def getLink(A):
    # This part intend to getting the problem link
    # if you enter getLink('E'), if may return the url whose text is 'E'
    # In case that it may be link on div 1, but problem on div 2, I do this part

    # find "/contest/1001/A" "/contest/1001/B/" etc
    for name in bsObj.find('table', {"class":"problems"}).findAll('a', {"href":re.compile("\/contest/[a-z0-9]*\/problem\/[a-zA-Z0-9]")}):
        # if it's exact what we want
        if name.get_text() == "\n                " + A + "\n            ":
            link = "https://codeforces.com" + name['href']
            return link

def getInput(A):
    numList = ["1", "2", "3", "4", "5"]
    i = 0
    Link = getLink(A)
    if Link is None:
        print("Success!")
        exit()
    thishtml = urlopen(Link)
    bsOBJ = BeautifulSoup(thishtml, features="html5lib")
    Filename = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g'}
    for name in bsOBJ.find_all("div", {"class":"input"}):
        input_file = open(Filename[A] + numList[i] + ".in", 'w')
        text = name.get_text()
        input_file.write(text[5:])
        i = i + 1
        # print("%r" % text)
        input_file.closed


def getOutput(A):
    numList = ["1", "2", "3", "4", "5"]
    i = 0
    Link = getLink(A)
    if Link is None:
        print("Success!")
        exit()
    thishtml = urlopen(Link)
    bsOBJ = BeautifulSoup(thishtml, features="html5lib")
    Filename = {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g'}
    for name in bsOBJ.find_all("div", {"class":"output"}):
        output_file = open(Filename[A] + numList[i] + ".out", 'w')
        text = name.get_text()
        output_file.write(text[6:])
        i = i + 1
        # print("%r" % text)
        output_file.closed

def getExamples(A):
    getInput(A)
    getOutput(A)

# This is the main program

Contest_id = input("Please Enter the Contest id:\n>")

## Get the contest main page
## url like: http://codeforces.com/contest/1001/
Contest_root_html = urlopen("http://codeforces.com/contest/" + Contest_id + "/")
bsObj = BeautifulSoup(Contest_root_html, features="html5lib")

## Processing Each problem
## url like: http://codeforces.com/contest/1001/problem/A
nameList = ["A", "B", "C", "D", "E", "F", "G"]

for name in nameList:
    print("Processing with " + name + " ...")
    getExamples(name)

