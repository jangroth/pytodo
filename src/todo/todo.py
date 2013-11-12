import datetime
import re

class Todo:
    '''
     Holds a single todo item with all its relevant information.
    '''
    
    def __init__(self, todoString, index=0):
        self.todoString = todoString
        self.index = index
        self.priority = ""
        self.goal = ""
        self.timeContext = ""
        self.projects = set()
        self.contexts = set()
        self.isMsd = False
        self.isNew = False
        workString = todoString;
        workString, self.timeContext, self.isMsd, self.isNew = self._cut_time_context(workString)
        workString, self.priority = self._cut_priority(workString)
        workString, self.projects = self._cut_uniqueStrings(workString, r'\+\S+', self.projects)
        workString, self.contexts = self._cut_uniqueStrings(workString, r'\@\S+', self.contexts)
        self.goal = workString.strip()
        self.isMalformed = self._check_for_malformed_warning()
        
    def _cut_time_context(self, stringToParse):
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

    def _cut_priority(self, stringToParse):
        '''
        Cuts out the priority, uses priority Z if no information found.
        '''
        result = '(Z)'
        match = re.compile(r'^\([A-Z]\)').search(stringToParse)
        if match:
            result = match.group()
            stringToParse = stringToParse.replace(result, "")
        return (stringToParse, result[1:2])
    
    def _cut_uniqueStrings(self, todoString, regExp, storingList):
        '''
        Cuts out a given regex and adds to provided list.
        '''
        regexp = re.compile(regExp)
        for match in regexp.finditer(todoString):
            found = match.group()
            if (found[1:] not in set(storingList)):
                storingList.add(found[1:])
                todoString = todoString.replace(found, "")
        return (todoString, storingList)
                
    def _check_for_malformed_warning(self):
        '''
        No project or context information will result in a warning.
        '''
        result = False
        if self.isNew == False:
            if len(self.projects) == 0 or len(self.contexts) == 0:
                print "- possibly malformed at line %s: %s" % (self.index, self.todoString)
                result = True
        return result

    def get_due_distance(self, comparisonDate=datetime.date.today()):
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
                testDate = comparisonDate + datetime.timedelta(weeks=(timeValue - comparisonWeek))
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

    def get_formatted_due_distance(self):
        result = ""
        distance = self.get_due_distance()
        if distance > 0:
            result = " (...{0}d)".format(distance)
        return result
    
    def get_category(self, comparisonDate=datetime.date.today()):
        '''
        Returns exactly one category (new  - current - future - past - msd) per todo item.
        '''
        result = ""
        if self.isNew:
            result = "new"
        elif self.isMsd == True:
            result = "msd"
        else:
            distance = self.get_due_distance(comparisonDate);
            if distance == 0: 
                result = "current"
            elif (distance > 0):
                result = "future"
            else:
                result = "past"
        return result
    
    def matches_project_or_context(self, project, context):
        '''
        If checks for match on project or context - if data is provided. Returns
        true otherwise.
        '''
        result = True
        if project != "":
            result = project in self.projects
        if context != "":
            result = context in self.contexts
        return result
    
    def get_sort_key(self):
        '''
        Used to determine the sort order of any two todos.
        '''
        return "%s %s %s" % (self.priority, 10000 + self.get_due_distance(), self.goal.lower());
    
    def get_print_string(self):
        '''
        Returns a printable string representation.
        '''
        return "(%s) - %s - +%s @%s %s" % (self.priority, self.goal.lower(), "-".join(a for a in self.projects), "-".join(a for a in self.contexts), self.get_formatted_due_distance())

if __name__ == "__main__":
    print "run todoIndicator.py"
