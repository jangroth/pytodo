import todo
import unittest

class KnownValues(unittest.TestCase):
    knownValues = ( ("some stuff", ["ddd"]),
                    ("some other stuff", ["ddd"]))

def should_extract_projects(self):
    for todoString, projects in self.knownValues:
        testTodo = todo.Todo(todoString)
        self.assertEqual(testTodo.projects, projects)
