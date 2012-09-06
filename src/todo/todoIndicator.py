#!/usr/bin/env python
from __future__ import division

import pygtk
pygtk.require('2.0')
import gtk
import os
import appindicator
import gobject
from todoList import TodoList

class TodoIndicator:
    '''
    GTK indicator that integrates in unity.
    '''
    def __init__(self, todoFileLocation):
        print "initializing..."
        self.todoFileLocation = todoFileLocation
        gobject.timeout_add(10, self._refresh_all, False)
        
    def _refresh_all(self, silent = True):
        self.todoList = TodoList(self.todoFileLocation);
        self.ind = self._get_indicator()
        self.menu = self._create_menu()
        self.ind.set_menu(self.menu)
        if silent == False:
            self.todoList.print_stats()
        gobject.timeout_add(10000, self._refresh_all)
        
    def _get_indicator(self):
        result = appindicator.Indicator("todo", "todo", appindicator.CATEGORY_APPLICATION_STATUS)
        result.set_status (appindicator.STATUS_ACTIVE)
        result.set_icon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "todo.png")
        return result
            
    def _create_menu(self):
        menu = gtk.Menu()
        menu = self._append_overview_menu(menu)
        menu = self._append_project_menu(menu)
        menu = self._append_context_menu(menu)
        menu = self._append_malformed_menu(menu)
        # update 
        item = gtk.MenuItem('Update now')
        item.connect("activate", self._update_all, None)
        menu.append(item)
        # quit
        item = gtk.MenuItem('Quit')
        item.connect("activate", self._quit, None)
        menu.append(item)
        
        menu.show_all()
        return menu
    
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

    def _append_project_menu(self, menu):
        for project in self.todoList.projects:
            dict = self.todoList.get_as_dictionary(project = project)
            item = gtk.MenuItem("+%s (%s)" % (project, self._getDictLen(dict)))
            item.set_submenu(self._create_submenu(dict))
            menu.append(item)
        menu.append(gtk.SeparatorMenuItem())
        return menu
            
    def _append_context_menu(self, menu):
        for context in self.todoList.contexts:
            dict = self.todoList.get_as_dictionary(context = context)
            item = gtk.MenuItem("@%s (%s)" % (context, self._getDictLen(dict)))
            item.set_submenu(self._create_submenu(dict))
            menu.append(item)
        menu.append(gtk.SeparatorMenuItem())
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
    
    def _create_submenu(self, dict):
        result = gtk.Menu()
        for category in dict.keys():
            menuItem = gtk.MenuItem("=== %s === (%s)" % (category, len(dict[category])))
            menuItem.set_sensitive(False)
            result.append(menuItem)
            for item in sorted(dict[category], key=lambda index : index.get_sort_key()):
                result.append(gtk.MenuItem(item.get_print_string()))
        return result
    
    def _getDictLen(self, dict):
        result = 0
        for lst in dict.keys():
            result += len(dict[lst])
        return result
    
    def _update_all(self, *args):
        print "updating..."
        self._refresh_all(False)
    
    def _quit(self, *args):
        print "bye..."
        gtk.main_quit()
        
    def main(self):
        gtk.main()

if __name__ == "__main__":
    TodoIndicator("/data/Dropbox/todo/todo.txt").main()