#!/usr/bin/env python
from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk
import os
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
        menu = self._create_overview_menu()
        menu.append(gtk.SeparatorMenuItem())
        # projects
        for projectRow in self.todoList.get_projects():
            # item = gtk.MenuItem("+%s (%s %s %s %s %s)" % (projectRow[0].ljust(10, " "), projectRow[1], projectRow[2], projectRow[3], projectRow[4], projectRow[5]))
            item = gtk.MenuItem("+%s" % (projectRow[0]))
            item.set_submenu(self._create_submenu(project = projectRow[0]))
            menu.append(item)
        menu.append(gtk.SeparatorMenuItem())
        # contexts
        for context in self.todoList.contexts:
            item = gtk.MenuItem("@" + context)
            item.set_submenu(self._create_submenu(context = context))
            menu.append(item)
        menu.append(gtk.SeparatorMenuItem())
        # update & quit 
        #TODO update
        item = gtk.MenuItem('Quit')
        item.connect("activate", gtk.main_quit, None)
        item.show()
        menu.append(item)
        return menu
    
    def _create_overview_menu(self):
        result = gtk.Menu()
        dict = self.todoList.get_as_dictionary()
        for category in dict.keys():
            catLength = len(dict[category])
            menuItem = gtk.MenuItem("=== %s === (%s)" % (category, catLength))
            menuItem.set_sensitive(catLength > 0)
            if catLength > 0: 
                subMenu = gtk.Menu()
                for item in sorted(dict[category], key=lambda index : index.get_sort_key()):
                    subMenu.append(gtk.MenuItem(item.get_print_string()))
                menuItem.set_submenu(subMenu)
            result.append(menuItem)
        return result
                
    def _create_submenu(self, project="", context=""):
        result = gtk.Menu()
        dict = self.todoList.get_as_dictionary(project, context)
        for category in dict.keys():
            menuItem = gtk.MenuItem("=== %s === (%s)" % (category, len(dict[category])))
            menuItem.set_sensitive(False)
            result.append(menuItem)
            for item in sorted(dict[category], key=lambda index : index.get_sort_key()):
                result.append(gtk.MenuItem(item.get_print_string()))
        return result
    
    def main(self):
        gtk.main()
