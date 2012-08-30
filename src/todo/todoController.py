#/usr/bin/env python
from todo import Todo
#import os

todoVar = "TODO_DIR_PYTHON"
todos = {'new':[], 'past': [], 'current':[], 'future':[], 'msd':[]}

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
        item = item[0:len(item) - 1]
        todo = Todo(item, index)
        todos[todo.getCategory()].append(todo)

def printTodos():
    '''todo'''
    print("---- new ----")
    for item in sorted(todos['new'], key=lambda index : index.getSortKey()):
        print(item.getPrintString());
    print("---- past ----")
    for item in sorted(todos['past'], key=lambda index : index.getSortKey()):
        print(item.getPrintString());
    print("---- current ----")
    for item in sorted(todos['current'], key=lambda index : index.getSortKey()):
        print(item.getPrintString());
    print("---- future ----")
    for item in sorted(todos['future'], key=lambda index : index.getSortKey()):
        print(item.getPrintString());
    print("---- msd ----")
    for item in sorted(todos['msd'], key=lambda index : index.getSortKey()):
        print(item.getPrintString());

if __name__ == "__main__":
    readDataFromFile()
    printTodos()
