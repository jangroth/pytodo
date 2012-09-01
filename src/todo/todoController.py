#/usr/bin/env python
from todo import Todo
from todoList import TodoList
#import os

todoVar = "TODO_DIR_PYTHON"
todos = {'new':[], 'past': [], 'current':[], 'future':[], 'msd':[]}

def getTodoPath():
    '''todo'''
    # return os.environ['TODO_DIR_PYTHON'] + "/todo.txt"
    # return "files/play.txt"
    return "/data/Dropbox/todo/todo.txt"
    
def readDataFromFile():
    '''read data file and dispatch into dictionary'''
    global todos
    todoFile = open(getTodoPath(), 'r')
    allTodos = todoFile.readlines()
    todoFile.close()
    todoList = TodoList(allTodos)
    todoList.printAsDictionary()

if __name__ == "__main__":
    readDataFromFile()
#    printTodos()
