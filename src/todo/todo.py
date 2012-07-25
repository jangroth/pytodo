#/usr/bin/env python
import datetime
import os
import re

todoVar = "TODO_DIR_PYTHON"
todos = {'inbox':[], 'future':[], 'past':[], 'msd':[]}

class Todo:
    ''' holds a todo with all its information'''
    def __init__(self, todoString, lineNumber = 0):
        self.todoString = todoString
        self.lineNumber = lineNumber
        self.dueDistance = 0
        self.priority = ""
        self.goal = ""
        self.timeContext = ""
        self.projects = []
        self.contexts = []
        todoString = self._cutTimeContext(todoString)
        todoString = self._cutPriority(todoString)
        todoString = self._cutUniqueStrings(todoString, r'\+\S+', self.projects)
        todoString = self._cutUniqueStrings(todoString, r'\@\S+', self.contexts)
        self.goal = todoString.strip()
        
    def _cutTimeContext(self, todoString):
        match = re.compile(r'\+_[myw]\d{2}').search(todoString)
        if match:
            found = match.group()
            self.timeContext = found[2:]
            todoString = todoString.replace(found, "")
        else:
            match = re.compile(r'\+_msd}').search(todoString)
            if match:
                self.isMsd = false
            
        return todoString

    def _cutPriority(self, todoString):
        result = '(Z)'
        match = re.compile(r'^\([ABCDEF]\)').search(todoString)
        if match:
            result = match.group()
            todoString = todoString.replace(result, "")
        self.priority = result
        return todoString
    
    def _cutUniqueStrings(self, todoString, regExp, storingList):
        regexp = re.compile(regExp)
        for match in regexp.finditer(todoString):
            found = match.group()
            if (found[1:] not in set(storingList)):
                storingList.append(found[1:])
                todoString = todoString.replace(found, "")
        return todoString
                
    def getDueDistance(self, comparisonDate = datetime.date.today()):
        result = 0
        quantifier = self.timeContext[0]
        timeValue = int(self.timeContext[1:3])
        comparisonYear = comparisonDate.isocalendar()[0]
        comparisonMonth = comparisonDate.month
        comparisonWeek = comparisonDate.isocalendar()[1]
        if quantifier == "w":
            testDate = comparisonDate + datetime.timedelta(weeks = (timeValue - comparisonWeek))
            result = testDate - comparisonDate
        elif quantifier == "m":
            extraYear = 0
            if comparisonMonth > timeValue:
                extraYear = 1
            testDate = datetime.date(comparisonYear + extraYear, timeValue, 1)
            result = testDate - comparisonDate
        elif quantifier == "y":
            timeValue += 2000
            testDate = datetime.date(timeValue, 1, 1)
            result = testDate - comparisonDate
        result = result.days
        return result
    
    def getCategory(self):
        result = ""
        if contexts.index("@inbox") > 0:
            result = "inbox"

def getTodoPath():
    '''todo'''
    # return os.environ['TODO_DIR_PYTHON'] + "/todo.txt"
    return "files/play.txt"
    
def readDataFromFile():
    '''read data file an dispatch into dictionary'''
    global todos
    todoFile = open(getTodoPath(), 'r')
    allTodos = todoFile.readlines()
    todoFile.close()
    for index, item in enumerate(allTodos):
        item = item[0:len(item)-1]
        todo = Todo(item, index)
        todos[todo.getCategory()].append(todo)
    

def printTodos():
    '''todo'''
    print("---- overdue ----")
    for item in todos['past']:
        print(item);
    print("---- scheduled ----")
    for item in todos['future']:
        print(item);
    print("---- msd ----")
    for item in todos['msd']:
        print(item);
    print("---- inbox ----")
    for item in todos['inbox']:
        print(item);

if __name__ == "__main__":
    readDataFromFile()
    printTodos()