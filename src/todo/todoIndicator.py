#!/usr/bin/env python
from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk
import os
import appindicator
from todoList import TodoList

#Parameters
MIN_WORK_TIME = 60 * 10 # min work time in seconds

class TodoIndicator:
    '''
    GTK indicator that integrates in unity.
    '''
    def __init__(self, todoFileLocation):
        print "initializing..."
        self.todoFileLocation = todoFileLocation
        self._refresh_all()
        
    def _refresh_all(self):
        self.todoList = TodoList(self.todoFileLocation);
        self.ind = self._get_indicator()
        self.menu = self._create_menu()
        self.ind.set_menu(self.menu)
        self.todoList.print_stats()
        
    def _get_indicator(self):
        result = appindicator.Indicator("todo", "todo", appindicator.CATEGORY_APPLICATION_STATUS)
        result.set_status (appindicator.STATUS_ACTIVE)
        result.set_icon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "todo.png")
        return result
            
    def _create_menu(self):
        menu = gtk.Menu()
        menu = self._append_overview_menu(menu)
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
        # malformed
        menu = self._append_malformed_menu(menu)
        # update 
        item = gtk.MenuItem('Upate')
        item.connect("activate", self._update_all, None)
        menu.append(item)
        # quit
        item = gtk.MenuItem('Quit')
        item.connect("activate", self._quit, None)
        menu.append(item)
        menu.show_all()
        return menu
    
    def _append_malformed_menu(self, menu):
        malformed = []
        for todo in self.todoList.todos:
            if todo.isMalformed == True:
                malformed.append(gtk.MenuItem("%s - %s" % (todo.index, todo.todoString)))
        if len(malformed) > 0:
            item = gtk.MenuItem("malformed (%s)" % (len(malformed)))
            subMenu = gtk.Menu()
            for malItem in malformed:            
                subMenu.append(malItem)
            item.set_submenu(subMenu)
            menu.append(item)    
            menu.append(gtk.SeparatorMenuItem())
        return menu
    
    def _update_all(self, *args):
        print "updating..."
        self._refresh_all()
    
    def _quit(self, *args):
        print "bye..."
        gtk.main_quit()
        
    def _append_overview_menu(self, menu):
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
            menu.append(menuItem)
        menu.append(gtk.SeparatorMenuItem())
        return menu
                
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

if __name__ == "__main__":
    TodoIndicator("/data/Dropbox/todo/todo.txt").main()