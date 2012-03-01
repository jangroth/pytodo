import unittest
import todo

class ProjectExtraction(unittest.TestCase):
    knownValues = ( ("my text is here +project ", ["project"]),
                    ("some other stuff +test +tast", ["test", "tast"]),
                    ("some other stuff +test +test", ["test"]),
                    ("some other stuff +real *test @tast", ["real"]),
                    ("some other stuff", []))

    def testProjectExtraction(self):
        for todoString, projects in self.knownValues:
            testTodo = todo.Todo(todoString)
            self.assertEqual(testTodo.projects, projects)
            
if __name__ == "__main__":
    unittest.main()
