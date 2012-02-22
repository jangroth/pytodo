#/usr/bin/env python
import datetime
import os
import re

todoVar = "TODO_DIR_PYTHON"
todos = {'inbox':[], 'future':[], 'past':[], 'msd':[]}

def getTodoPath():
    '''todo'''
    # return os.environ['TODO_DIR_PYTHON'] + "/todo.txt"
    return "play.txt"
    
def readDataFromFile():
    '''read data file an dispatch into dictionary'''
    global todos
    todoFile = open(getTodoPath(), 'r')
    allTodos = todoFile.readlines()
    todoFile.close()
    for item in allTodos:
        item = item[0:len(item)-1]
        if re.compile(r'\+_msd').search(item):
            todos['msd'].append(item)
        elif re.compile(r'\+_[myw]\d{2}').search(item):
            if (getTimeDistanceInDays(item) < 0):
                todos['past'].append(item)
            else:
                todos['future'].append(item)
        else:
            todos['inbox'].append(item)
        todos['past'].sort(listComparator)
    
def getTimeDistanceInDays(item, date = '12'):
    result = 0
    match = re.compile(r'\+_[myw]\d{2}').search(item)
    if match:
        timeContext = match.group()
        quantifier = timeContext[2]
        timeValue = int(timeContext[3:5])
        currentDate = datetime.date.today()
        currentYear = currentDate.isocalendar()[0]
        currentMonth = currentDate.month
        currentWeek = currentDate.isocalendar()[1]
        if quantifier == "w":
            testDate = currentDate + datetime.timedelta(weeks = (timeValue - currentWeek))
            result = testDate - currentDate
        elif quantifier == "m":
            extraYear = 0
            if currentMonth > timeValue:
                extraYear = 1
            testDate = datetime.date(currentYear + extraYear, timeValue, 1)
            result = testDate - currentDate
        elif quantifier == "y":
            timeValue += 2000
            testDate = datetime.date(timeValue, 1, 1)
            result = testDate - currentDate
        else:
            print "problem"
        result = result.days
    return result

def getPriority(item):
    result = '(Z)'
    match = re.compile(r'^\([ABCDEF]\)').search(item)
    if match:
        result = match.group()
    return result

def listComparator(item1, item2):
    dist1 = getTimeDistanceInDays(item1)
    dist2 = getTimeDistanceInDays(item2)
    result = cmp(dist1, dist2)
    if (result == 0):
        prio1 = getPriority(item1)
        prio2 = getPriority(item2)
        result = cmp(prio1, prio2)
    return result

def printSingleLine(item):
    print repr(getTimeDistanceInDays(item)).rjust(4), repr(getPriority(item)).rjust(4), item
    

def printTodos():
    '''todo'''
    print "---- overdue ----"
    for item in todos['past']:
        printSingleLine(item);
    print "---- scheduled ----"
    for item in todos['future']:
        printSingleLine(item);
    print "---- msd ----"
    for item in todos['msd']:
        printSingleLine(item);
    print "---- inbox ----"
    for item in todos['inbox']:
        printSingleLine(item);

if __name__ == "__main__":
    readDataFromFile()
    printTodos()
#    printTodos(todos)
#    todos.sort(listComparator)
#    print "-------"
#    printTodos(todos)
