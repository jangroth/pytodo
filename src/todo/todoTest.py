import unittest
import todo
import datetime

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
            
class ContextExtraction(unittest.TestCase):
    knownValues = ( ("my text is here @context ", ["context"]),
                    ("some other stuff @test @tast", ["test", "tast"]),
                    ("some other stuff @test @test", ["test"]),
                    ("some other stuff +real *test @tast", ["tast"]),
                    ("some other stuff", []))

    def testContextExtraction(self):
        for todoString, contexts in self.knownValues:
            testTodo = todo.Todo(todoString)
            self.assertEqual(testTodo.contexts, contexts)
            
class PriorityExtraction(unittest.TestCase):
    knownValues = ( ("my text is here", "(Z)"),
                    ("(A) some other stuff @test @tast", "(A)"),
                    ("(B) some other stuff @test @tast", "(B)"),
                    ("(C) some other stuff @test @tast", "(C)"),
                    ("(D) some other stuff @test @tast", "(D)"),
                    ("(E) some other stuff @test @tast", "(E)"),
                    ("(F) some other stuff @test @tast", "(F)"),
                    ("(G) some other stuff @test @tast", "(Z)"))

    def testPriorityExtraction(self):
        for todoString, priority in self.knownValues:
            testTodo = todo.Todo(todoString)
            self.assertEqual(testTodo.priority, priority)
            
class TimeContextExtraction(unittest.TestCase):
    knownValues = ( ("my text is here", "new", False, True),
                    ("(A) some other stuff +_w12", "w12", False, False),
                    ("(B) some other stuff +_m10", "m10", False, False),
                    ("(C) some other stuff +_y14", "y14", False, False),
                    ("(C) some other stuff +_msd", "msd", True, False),
                    ("(D) some other stuff +_w11 @tast", "w11", False, False))

    def testTimeContextExtraction(self):
        for todoString, timeContext, isMsd, isNew in self.knownValues:
            testTodo = todo.Todo(todoString)
            self.assertEqual(testTodo.timeContext, timeContext)
            self.assertEqual(testTodo.isMsd, isMsd)
            self.assertEqual(testTodo.isNew, isNew)
            
class GoalExtraction(unittest.TestCase):
    knownValues = ( ("my text is here", "my text is here"),
                    ("(A) some other stuff +_w12", "some other stuff"),
                    ("(D) some other stuff +_w11 @tast", "some other stuff"))

    def testTimeContextExtraction(self):
        for todoString, goal in self.knownValues:
            testTodo = todo.Todo(todoString)
            self.assertEqual(testTodo.goal, goal)

class DueDateTest(unittest.TestCase):
    knownValues = ( ("m03",-6),
                    ("m04",25),
                    ("w09",-7),
                    ("w10",0),
                    ("w11",7),
                    ("y12",-66),
                    ("y13",300),
                    ("", 0))             
    def testDifferentDueDates(self):
        comparisonDate = datetime.date(2012,3,7)
        for timeString, result in self.knownValues:
            testTodo = todo.Todo("some dummy stuff +_" + timeString)
            self.assertEqual(testTodo.getDueDistance(comparisonDate), result)

if __name__ == "__main__":
    unittest.main()
