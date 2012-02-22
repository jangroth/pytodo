#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
 
def sayHello():
    print "Hello World!"
 
# Create the Qt Application
app = QApplication(sys.argv)
# Create a button, connect it and show it
button = QPushButton("Click me")
button.clicked.connect(sayHello)
button.show()
# Run the main Qt loop
app.exec_()    