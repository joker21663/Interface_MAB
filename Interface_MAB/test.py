#!/usr/bin/env python

# import libraries
import gtk
import sys,os
import linuxcnc, hal
import gladevcp.makepins

# set up paths to files
BASE = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
libdir = os.path.join(BASE, "lib", "python")
sys.path.insert(0, libdir)
datadir = os.path.join(BASE, "share", "linuxcnc")
xmlname = os.path.join(datadir,"gui6.glade")

# main class
class gui6(object):
  def __init__(self):
    self.builder = gtk.Builder()
    self.builder.add_from_file(xmlname)
    self.builder.connect_signals(self)
    self.window = self.builder.get_object("window1")
    self.halcomp = hal.component("gui6")
    self.panel = gladevcp.makepins.GladePanel(self.halcomp, xmlname, self.builder, None)
    self.halcomp.ready()
    self.window.show()

  # create methods to handle the signal handlers

  def on_window1_destroy(self, widget, data=None):
    print "quit with cancel"
    gtk.main_quit()

  def on_menu_quit_activate(self, menuitem, data=None):
    print "quit from menu"
    gtk.main_quit()

# run the program
if __name__ == "__main__":
  app = gui6() # initialize an instance of the gui6 class called app
  gtk.main() # start monitoring signals from our program