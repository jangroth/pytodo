#!/usr/bin/env python
from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk
import os
from datetime import timedelta
from time import time
from math import floor
gtk.gdk.threads_init()
import gobject
import appindicator

#Parameters
MIN_WORK_TIME = 60 * 10 # min work time in seconds

class TodoIndicator:
    def __init__(self, todoList):
        self.todoList = todoList;
        self.ind = appindicator.Indicator("todo", "todo", appindicator.CATEGORY_APPLICATION_STATUS)

        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_icon(self.icon_directory() + "todo.png")
        self.menu = self._create_menu()
        self.menu.show_all()
        self.ind.set_menu(self.menu)
    def icon_directory(self):
        return os.path.dirname(os.path.realpath(__file__)) + os.path.sep 
    def _create_menu(self):
        menu = gtk.Menu()
        # projects
        for projectRow in self.todoList.get_projects():
            item = gtk.MenuItem("+%s (%s %s %s %s)" % (projectRow[0].ljust(15," "), projectRow[1], projectRow[2], projectRow[3], projectRow[4]))
            subMenu = gtk.Menu()
            subItem = gtk.MenuItem("sub")
            subMenu.append(subItem)
            item.set_submenu(subMenu)
            menu.append(item)
        separator = gtk.SeparatorMenuItem()
        separator.show()
        menu.append(separator)
        # contexts
        for context in self.todoList.contexts:
            item = gtk.MenuItem("@" + context)
            item.show()
            menu.append(item)
        # Tooltip item
        # A separator
        separator = gtk.SeparatorMenuItem()
        separator.show()
        menu.append(separator)
        # A quit item
        item = gtk.MenuItem('Quit')
        item.connect("activate", gtk.main_quit, None)
        item.show()
        menu.append(item)
        return menu
    
    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        # source_id = gobject.timeout_add(self.tick_interval, self.update)
        gtk.main()