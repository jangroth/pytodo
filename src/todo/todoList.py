import datetime
from todo import Todo

class TodoList:
    '''
    Parses a todo.txt file, holds all items, provides filtering & grouping operations.
    '''
    def __init__(self, filePath):
        self.filePath = filePath
        self.refresh()

    def _read_todos(self, filePath):
        '''
        Returns all lines of the given todo.txt file.
        '''
        todoFile = open(filePath, 'r')
        allLines = todoFile.readlines()
        todoFile.close()
        return allLines

    def refresh(self):
        '''
        (re-)loads and parses list of todos.
        '''
        self.rawLines = self._read_todos(self.filePath)
        self.todos = []
        self.projects = set()
        self.contexts = set()
        for index, item in enumerate(self.rawLines):
            item = item[0:len(item) - 1]
            todo = Todo(item, index + 1)
            self.todos.append(todo)
            self.projects = self.projects.union(todo.projects)
            self.contexts = self.contexts.union(todo.contexts)

    def get_as_dictionary(self, project="", context="", comparisonDate=datetime.date.today()):
        '''
        Returns fixed dictionary of time category (key) and todo (value), uses filter if provided. 
        '''
        result = {'past':[], 'current':[], 'future':[], 'new':[], 'msd':[], }
        for todo in self.todos:
            if todo.matches_project_or_context(project, context):
                result[todo.get_category(comparisonDate)].append(todo)
        return result

    def print_as_dictionary(self, project="", context="", comparisonDate=datetime.date.today()):
        '''
        Prints dictionary of time category (key) and todo list (value), uses filter if provided. Mainly 
        useful for debugging purposes. 
        '''
        dict = self.get_as_dictionary(project, context, comparisonDate)
        for category in dict.keys():
            print "============= %s =============" % (category)
            for item in sorted(dict[category], key=lambda index : index.get_sort_key()):
                print "%s" % item.get_print_string()

    def print_stats(self):
        '''
        Prints basic statistic about list of todos.
        '''
        print "Found %s todos at %s" % (len(self.todos), self.filePath)
        print "%s projects (%s)" % (len(self.projects), "-".join(a for a in self.projects))
        print "%s contexts (%s)" % (len(self.contexts), "-".join(a for a in self.contexts))

if __name__ == "__main__":
    print "run todoIndicator.py"
