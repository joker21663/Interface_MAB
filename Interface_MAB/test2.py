#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk, os

class App:
  def __init__(self):
    # Всякая унылая хрень
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.window.connect("destroy", gtk.main_quit)
    self.window.set_size_request(200, 100)
    self.liststore = gtk.ListStore(str)
    self.treeview = gtk.TreeView(self.liststore)
    self.treeview.connect('key-press-event', self.on_key_press)
    # 1 колонка
    tvcolumn = gtk.TreeViewColumn("Column 1")
    cell = gtk.CellRendererText()
    cell.set_property('editable', True)
    tvcolumn.pack_start(cell, True)
    tvcolumn.set_attributes(cell, text=0)
    self.treeview.append_column(tvcolumn)
    # 2 строки
    self.liststore.append(["row1"])
    self.liststore.append(["row2"])
    # Запускаем
    self.window.add(self.treeview)
    self.window.show_all()

  def on_key_press(self, widget, event):
    keyname = gtk.gdk.keyval_name(event.keyval)
    if keyname == 'Tab':
      column = self.treeview.get_column(0)
      self.treeview.set_cursor((0,), column, start_editing = True)
      # self.treeview.grab_focus() # Если не убрать, то не работает
      return True # Чтобы не обрабатывался дальше Tab

  def main(self):
    gtk.main()

if __name__ == "__main__":
  app = App()
  app.main()