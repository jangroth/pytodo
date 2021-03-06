#!/usr/bin/env python

from __future__ import division
from subprocess import Popen
import pygtk
pygtk.require('2.0')
import gtk
import os
import appindicator
import gobject
import sys

from todoList import TodoList

defaultFileLocation = "/data/Dropbox/documents/todo.txt"

class TodoIndicator:
    '''
    GTK indicator that integrates in Unity.

    Example usage: ./todoIndicator.py TODO_FILE_LOCATION

    If no value for TODO_FILE_LOCATION is provided, a file named 'todo.txt' will be
    loaded from the directory specified in the environment variable TODO_DIR. If this
    variable does not exist, the file will be loaded from a hard coded default location.
    '''
    def __init__(self, todoFileLocation):
        self.todoFileLocation = todoFileLocation
        gobject.timeout_add(10, self._refresh_all, False)

    def _refresh_all(self, silent = True):
        self.todoList = TodoList(self.todoFileLocation);
        self.ind = self._get_indicator()
        self.menu = self._create_menu()
        self.ind.set_menu(self.menu)
        if silent == False:
            self.todoList.print_stats()

    def _get_indicator(self):
        result = appindicator.Indicator("todo", "todo", appindicator.CATEGORY_APPLICATION_STATUS)
        result.set_status (appindicator.STATUS_ACTIVE)
        result.set_icon(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "todo.png")
        return result

    def _create_menu(self):
        menu = gtk.Menu()
        # update
        item = gtk.MenuItem('Update now')
        item.connect("activate", self._update_all, None)
        menu.append(item)
        # open file
        item = gtk.MenuItem('Edit todo.txt')
        item.connect("activate", self._open_file, 1)
        menu.append(item)
        menu.append(gtk.SeparatorMenuItem())
        menu = self._append_overview_menu(menu)
        menu = self._append_project_menu(menu)
        menu = self._append_context_menu(menu)
        menu = self._append_malformed_menu(menu)
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
                    subMenu.append(self._get_menu_item_from_todo(item))
                menuItem.set_submenu(subMenu)
            menu.append(menuItem)
        menu.append(gtk.SeparatorMenuItem())
        return menu

    def _append_project_menu(self, menu):
        for project in sorted(self.todoList.projects, key = self.todoList.openTodosForProject, reverse = True):
            dict = self.todoList.get_as_dictionary(project = project)
            menuItem = gtk.MenuItem("+%s (%s)" % (project, self.todoList.openTodosForProject(project)))
            menuItem.set_submenu(self._create_submenu(dict))
            menu.append(menuItem)
        menu.append(gtk.SeparatorMenuItem())
        return menu

    def _append_context_menu(self, menu):
        for context in sorted(self.todoList.contexts, key = self.todoList.openTodosForContext, reverse = True):
            dict = self.todoList.get_as_dictionary(context = context)
            menuItem = gtk.MenuItem("@%s (%s)" % (context, self.todoList.openTodosForContext(context)))
            menuItem.set_submenu(self._create_submenu(dict))
            menu.append(menuItem)
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
                result.append(self._get_menu_item_from_todo(item))
        return result

    def _get_menu_item_from_todo(self, todo):
        result = gtk.MenuItem(todo.get_print_string())
        result.connect("activate", self._open_file, todo.index)
        return result

    def _update_all(self, *args):
        print "updating..."
        self._refresh_all(False)

    def _open_file(self, *args):
        print "opening editor..."
        Popen(["gvim", "+%s" % (args[1]), self.todoFileLocation], stdin=open(os.devnull, 'r'))

    def _quit(self, *args):
        print "bye..."
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    fileLocation = defaultFileLocation
    if len(sys.argv) >= 2:
        fileLocation = sys.argv[1]
    elif 'TODO_DIR' in os.environ:
        fileLocation = os.environ['TODO_DIR'] + "/todo.txt"
    TodoIndicator(fileLocation).main()
