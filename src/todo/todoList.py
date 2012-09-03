import datetime
from todo import Todo
from collections import defaultdict

class TodoList:
    '''
    Holds a list of todo items and provides filtering & grouping operations.
    '''
    def __init__(self, listOfRawStrings=[]):
        self.todoList = []
        self.projects = set()
        self.contexts = set()
        for index, item in enumerate(listOfRawStrings):
            item = item[0:len(item) - 1]
            todo = Todo(item, index + 1)
            self.todoList.append(todo)
            self.projects = self.projects.union(todo.projects)
            self.contexts = self.contexts.union(todo.contexts)
    
    def _filter(self, todo, project, context):
        result = True
        if project != "":
            result = project in todo.projects
        if context != "":
            result = context in todo.contexts
        return result
    
    def get_projects(self):
        result = []
        projects = sorted(self.projects)
        for project in projects:
            projDict = self.get_as_dictionary(project)
            row = [project]
            for item in sorted(projDict.iterkeys()):
                row.append(item[0:2] + ":"+ str(len(projDict[item])))
            result.append(row)
        print result
        return result
    
    def get_as_dictionary(self, project="", context="", comparisonDate=datetime.date.today()):
        #result = defaultdict(list)
        result = {'past':[],'current':[],'future':[],'new':[],'msd':[],}
        for todo in self.todoList:
            if self._filter(todo, project, context):
                result[todo.get_category(comparisonDate)].append(todo)
        return result
    
    def print_as_dictionary(self, project="", context="", comparisonDate=datetime.date.today()):
        dict = self.get_as_dictionary(project, context, comparisonDate)
        for category in dict.keys():
            print "============= %s =============" % (category)
            for item in sorted(dict[category], key=lambda index : index.get_sort_key()):
                print "%s" % item.get_print_string()
                
    def print_stats(self):
        print "%s todos" % (len(self.todoList))
        print "%s projects (%s)" % (len(self.projects), "-".join(a for a in self.projects))
        print "%s contexts (%s)" % (len(self.contexts), "-".join(a for a in self.contexts))
    
        
        
        
    
