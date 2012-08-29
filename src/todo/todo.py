#/usr/bin/env python
import datetime
import os
import re
#from chardet.test import result

todoVar = "TODO_DIR_PYTHON"
todos = {'inbox':[], 'future':[], 'current':[], 'past':[], 'msd':[]}

class Todo:
    '''
     Holds a single todo item with all its relevant information.
    '''
    def __init__(self, todoString, lineNumber = 0):
        self.todoString = todoString
        self.lineNumber = lineNumber
        self.dueDistance = 0
        self.priority = ""
        self.goal = ""
        self.timeContext = ""
        self.projects = []
        self.contexts = []
        self.isMsd = False
        todoString, self.timeContext, self.isMsd = self._cutTimeContext(todoString)
        todoString, self.priority = self._cutPriority(todoString)
        todoString, self.projects = self._cutUniqueStrings(todoString, r'\+\S+', self.projects)
        todoString, self.contexts = self._cutUniqueStrings(todoString, r'\@\S+', self.contexts)
        self.goal = todoString.strip()
        
    def _cutTimeContext(self, stringToParse):
        '''
        Cuts out the time context.
        '''
        result = ""
        isMsd = False
        match = re.compile(r'\+_[myw]\d{2}').search(stringToParse)
        if match:
            found = match.group()
            result = found[2:]
            stringToParse = stringToParse.replace(found, "")
        else:
            match = re.compile(r'\+_msd').search(stringToParse)
            if match:
                result = "msd"
                isMsd = True
        return (stringToParse, result, isMsd)

    def _cutPriority(self, stringToParse):
        '''
        Cuts out the priority, uses Z if not set.
        '''
        result = '(Z)'
        match = re.compile(r'^\([ABCDEF]\)').search(stringToParse)
        if match:
            result = match.group()
            stringToParse = stringToParse.replace(result, "")
        return (stringToParse, result)
    
    def _cutUniqueStrings(self, todoString, regExp, storingList):
        '''
        Cuts out a given regex and adds to provided list.
        '''
        regexp = re.compile(regExp)
        for match in regexp.finditer(todoString):
            found = match.group()
            if (found[1:] not in set(storingList)):
                storingList.append(found[1:])
                todoString = todoString.replace(found, "")
        return (todoString, storingList)
                
    def getDueDistance(self, comparisonDate = datetime.date.today()):
        '''
        Evaluates the timeContext and calculates distance to either the 
        provided comparison data or the current date.
        '''
        result = 0
        if self.timeContext != "":
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
    
    def getCategory(self, comparisonDate = datetime.date.today()):
        result = ""
        if "inbox" in self.contexts:
            result = "inbox"
        else:
            distance = self.getDueDistance(comparisonDate);
            if distance == 0: 
                result = "current"
            elif distance > 0:
                result = "future"
            else:
                result = "past"
        return result

def getTodoPath():
    '''todo'''
    # return os.environ['TODO_DIR_PYTHON'] + "/todo.txt"
    return "files/play.txt"
    
def readDataFromFile():
    '''read data file and dispatch into dictionary'''
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