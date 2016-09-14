# helloWorld

import datetime
from subprocess import call
import os
import gitapi
import urllib2
from BeautifulSoup import BeautifulSoup

commit_plan_file_name = 'date-wise-commit-plan.txt'
edit_file_name = 'Jaanu.txt'
pointer_line = 0
commit_colour_code = {0: 0, 1: 1, 2: 3, 3: 5, 4: 7}
commit_year = '2016'
quote_url = 'http://www.dailyinspirationalquotes.in/'


def get_daily_quotation(quote_number):
    page = urllib2.urlopen(quote_url)
    soup = BeautifulSoup(page.read())
    print str(soup.findAll("div",{"class":"td-excerpt"})[quote_number].contents[0]).replace('&#039;', '\'')
    return str(soup.findAll("div",{"class":"td-excerpt"})[quote_number].contents[0]).replace('&#039;', '\'')


def commit(number_of_commits, day, month):
    repo = gitapi.Repo("../gitCommitGridDrawing")
    # print repo.git_status()['??']
    # print repo.git_status()['AM']
    if repo.git_status().has_key('M'):
        for filename in repo.git_status()['M']:
            repo.git_add(filename)
    # Do the commit action
    for i in range(number_of_commits):
        edit_file = open(edit_file_name, 'a')
        quote_text = get_daily_quotation(i)
        edit_file.write(quote_text)
        edit_file.write("\n\t\t Quote on "+str(day)+"/"+str(month)+"/"+commit_year+"\n\n\n")
        edit_file.close()
        repo.git_add(edit_file_name)
        repo.git_commit(message="Modified edit file.")

    # print the log for verification of the commits made.
    # print repo.git_log()

def override_commit(number_of_commits, day, month, start_quote_num):
    repo = gitapi.Repo("../gitCommitGridDrawing")
    if repo.git_status().has_key('M'):
        for filename in repo.git_status()['M']:
            repo.git_add(filename)
    # Do the commit action
    for i in range(start_quote_num,number_of_commits+start_quote_num):
        edit_file = open(edit_file_name, 'a')
        quote_text = get_daily_quotation(i)
        edit_file.write(quote_text)
        edit_file.write("\n\t\t Quote on "+str(day)+"/"+str(month)+"/"+commit_year+"\n\n\n")
        edit_file.close()
        repo.git_add(edit_file_name)
        repo.git_commit(message="Modified file.")

    # print the log for verification of the commits made.
    # print repo.git_log()

def explore_repo():
    repo = gitapi.Repo("../gitCommitGridDrawing")
    print repo.git_status()['M']#['??']
    for x in repo.git_status()['M']:
        print x
    # print repo.git_status()['AM']


def run():
    now = datetime.datetime.now()
    datafile = open(commit_plan_file_name, 'r+')

    lines = datafile.readlines()
    line_pointer = int(lines[pointer_line])

    # Look for the concerned date colour code
    items = lines[line_pointer].split()
    while now.day != int(items[0]):
        line_pointer += 1
        items = lines[line_pointer].split()

    # Update the data file with the line pointer.
    datafile.seek(0)
    datafile.write('%05d' % line_pointer)

    # Check if the month matches
    if now.month != int(items[1]):
        raise Exception('Month not matching.')

    # Get the number of commits to be done for the concerned date.
    colour_code = int(items[2])
    number_of_commits = commit_colour_code[colour_code]
    print commit_colour_code[colour_code]

    # Go ahead and commit the required number of times.
    commit(number_of_commits, now.day, now.month)


def run2():
    # print urllib2.urlopen("http://stackoverflow.com/questions/29723419/python-anywhere-issue-using-urllib2-with-virtualenv").read()
    print get_daily_quotation(0)


def run3():
    explore_repo()


def run4():
    override_commit(1,10,9,2)


def commit_with_amend(date, month,day,colour_code,start_quote_num=0):
    repo = gitapi.Repo("../gitCommitGridDrawing")
    number_of_commits = commit_colour_code[colour_code]
    if repo.git_status().has_key('M'):
        for filename in repo.git_status()['M']:
            repo.git_add(filename)
    for i in range(start_quote_num,number_of_commits+start_quote_num):
        edit_file = open(edit_file_name, 'a')
        quote_text = get_daily_quotation(i)
        edit_file.write(quote_text)
        edit_file.write("\n\t\t Quote on "+str(date)+"/"+str(month)+"/"+commit_year+"\n\n\n")
        edit_file.close()
        repo.git_add(edit_file_name)
        repo.git_commit(message="Modified file.")
        #strarg = "commit --amend --date=\""+day+" "+month+" "+str(date)+" 19:0"+str(i)+" 2016 +0010\" "


def old_date_commit(date, month, day, colour_code, start_quote_num):
    commit_with_amend( date, month, day, colour_code, start_quote_num)


def run5():
    old_date_commit(14, 'Sep', 'Wed', 1, 0)


run5()
