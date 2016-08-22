# helloWorld

import datetime
import os
import gitapi

commit_plan_file_name = 'date-wise-commit-plan.txt'
edit_file_name = 'Jaanu.txt'
pointer_line = 0
commit_colour_code = {0: 0, 1: 1, 2: 3, 3: 5, 4: 7}
commit_year = '2016'


def commit(number_of_commits, day, month):
    repo = gitapi.Repo("../gitCommitGridDrawing")
    # print repo.git_status()['??']
    # print repo.git_status()['AM']

    # Do the commit action
    for i in range(number_of_commits):
        edit_file = open(edit_file_name, 'a')
        edit_file.write("Hello World. "+str(i+1)+"th commit on "+str(day)+"/"+str(month)+"/"+commit_year+"\n")
        edit_file.close()
        repo.git_add(edit_file_name)
        repo.git_commit(message="Modified dummy edit file.")

    # print the log for verification of the commits made.
    print repo.git_log()


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
    datafile.write('%05d' % (line_pointer+1))

    # Check if the month matches
    if now.month != int(items[1]):
        raise Exception('Month not matching.')

    # Get the number of commits to be done for the concerned date.
    colour_code = int(items[2])
    number_of_commits = commit_colour_code[colour_code]
    print commit_colour_code[colour_code]

    # Go ahead and commit the required number of times.
    commit(number_of_commits, now.day, now.month)

run()
