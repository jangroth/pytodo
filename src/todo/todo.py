#/usr/bin/env python
import datetime
import os
import re
#from chardet.test import result

todoVar = "TODO_DIR_PYTHON"
todos = {'new':[], 'past': [], 'current':[], 'future':[], 'msd':[]}

class Todo:
    '''
     Holds a single todo item with all its relevant information.
    '''
    def __init__(self, todoString, index = 0):
        self.todoString = todoString
        self.index = index
        self.priority = ""
        self.goal = ""
        self.timeContext = ""
        self.projects = []
        self.contexts = []
        self.isMsd = False
        self.isNew = False
        workString = todoString;
        workString, self.timeContext, self.isMsd, self.isNew = self._cutTimeContext(workString)
        workString, self.priority = self._cutPriority(workString)
        workString, self.projects = self._cutUniqueStrings(workString, r'\+\S+', self.projects)
        workString, self.contexts = self._cutUniqueStrings(workString, r'\@\S+', self.contexts)
        self.goal = workString.strip()
        
    def _cutTimeContext(self, stringToParse):
        '''
        Cuts out the time context.
        '''
        result = ""
        found = ""
        isMsd = False
        isNew = False
        match = re.compile(r'\+_[myw]\d{2}').search(stringToParse)
        if match:
            found = match.group()
            result = found[2:]
        else:
            match = re.compile(r'\+_msd').search(stringToParse)
            if match:
                found = match.group()
                result = "msd"
                isMsd = True
            else:
                match = re.compile(r'\+_\S+').search(stringToParse)
                if match: 
                    found = match.group()
                result = "new"
                isNew = True
        stringToParse = stringToParse.replace(found, "")
                
        return (stringToParse, result, isMsd, isNew)

    def _cutPriority(self, stringToParse):
        '''
        Cuts out the priority, uses Z if not set.
        '''
        result = '(Z)'
        match = re.compile(r'^\([A-Z]\)').search(stringToParse)
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
        if self.timeContext != "" and self.isMsd == False and self.isNew == False:
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
        if self.isNew:
            result = "new"
        elif self.isMsd == True:
            result = "msd"
        else:
            distance = self.getDueDistance(comparisonDate);
            if distance == 0: 
                result = "current"
            elif (distance > 0):
                result = "future"
            else:
                result = "past"
        return result
    
    def getSortKey(self):
        return "%s %s %s" % (self.priority, 10000 + self.getDueDistance(), self.goal.lower());
        # return self.getDueDistance()
    
    def getPrintString(self):
        return "%s - (%s:%s) - %s - %s" % (self.index, self.timeContext, self.getDueDistance(), self.priority, self.goal)

def getTodoPath():
    '''todo'''
    # return os.environ['TODO_DIR_PYTHON'] + "/todo.txt"
    return "/data/Dropbox/todo/todo.txt"
    # return "files/play.txt"
    
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
    print("---- new ----")
    for item in sorted(todos['new'], key = lambda index : index.getSortKey()):
        print(item.getPrintString());
    print("---- past ----")
    for item in sorted(todos['past'], key = lambda index : index.getSortKey()):
        print(item.getPrintString());
    print("---- current ----")
    for item in sorted(todos['current'], key = lambda index : index.getSortKey()):
        print(item.getPrintString());
    print("---- future ----")
    for item in sorted(todos['future'], key = lambda index : index.getSortKey()):
        print(item.getPrintString());
    print("---- msd ----")
    for item in sorted(todos['msd'], key = lambda index : index.getSortKey()):
        print(item.getPrintString());

if __name__ == "__main__":
    readDataFromFile()
    printTodos()