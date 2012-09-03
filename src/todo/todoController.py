#/usr/bin/env python
from todo import Todo
from todoList import TodoList
from todoIndicator import TodoIndicator
#import os

todoVar = "TODO_DIR_PYTHON"

def get_todo_path():
    '''todo'''
    # return os.environ['TODO_DIR_PYTHON'] + "/todo.txt"
    # return "files/play.txt"
    return "/data/Dropbox/todo/todo.txt"
    
def read_data_from_file():
    '''read data file and dispatch into dictionary'''
    todoFile = open(get_todo_path(), 'r')
    allTodos = todoFile.readlines()
    todoFile.close()
    todoList = TodoList(allTodos)
    return todoList

if __name__ == "__main__":
    todoList = read_data_from_file()
    todoList.print_stats()
    todoList.get_projects()
    todoList.print_as_dictionary()
    app = TodoIndicator(todoList)
    app.main()
