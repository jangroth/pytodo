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
    '''
    GTK indicator that integrates in unity.
    '''
    def __init__(self, todoList):
        self.todoList = todoList;
        self.ind = appindicator.Indicator("todo", "todo", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.ind.set_icon(self._icon_directory() + "todo.png")
        self.menu = self._create_menu()
        self.menu.show_all()
        self.ind.set_menu(self.menu)

    def _icon_directory(self):
        return os.path.dirname(os.path.realpath(__file__)) + os.path.sep 
    
    def _create_menu(self):
        menu = self._create_overview_menu()
        menu.append(gtk.SeparatorMenuItem())
        # projects
        for project in self.todoList.projects:
            item = gtk.MenuItem("+" + project)
            item.set_submenu(self._create_submenu(project = project))
            menu.append(item)
        menu.append(gtk.SeparatorMenuItem())
        # contexts
        for context in self.todoList.contexts:
            item = gtk.MenuItem("@" + context)
            item.set_submenu(self._create_submenu(context = context))
            menu.append(item)
        menu.append(gtk.SeparatorMenuItem())
        # update 
        item = gtk.MenuItem('Upate')
        item.connect("activate", self._update_all, None)
        menu.append(item)
        # quit
        item = gtk.MenuItem('Quit')
        item.connect("activate", gtk.main_quit, None)
        menu.append(item)
        return menu
    
    def _update_all(self, *args):
        print "update"
        self.todoList.refresh()
        self.__init__(self.todoList) 
    
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
