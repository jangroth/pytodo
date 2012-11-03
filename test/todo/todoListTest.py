import unittest
from todoList import TodoList

class AddTodos(unittest.TestCase):
    knownValues = ({"todo1 ", "todo2 ", "todo3 "}, 3)
    def testFilterForNothing(self):
        todoList = TodoList(self.knownValues[0])
        self.assertEqual(len(todoList.getAsDictionary()['new']), self.knownValues[1])

class SimpleteFiltering(unittest.TestCase):
    knownValues = ["todo1 +a @a ", "todo2 +a +b @a @b ", "todo3 "]
    def testFilterForNothing(self):
        todoList = TodoList(self.knownValues)
        print todoList.projects
        self.assertEqual(len(todoList.projects), 2)
        self.assertEqual(len(todoList.contexts), 2)

if __name__ == "__main__":
    unittest.main()
        
