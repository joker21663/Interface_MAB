#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
try:
     import pygtk
     pygtk.require("2.0")
except:
      pass
try:
    import gtk
    import gtk.glade
    import hal
    import gladevcp.makepins
    from gladevcp.gladebuilder import GladeBuilder
except:
    sys.exit(1)
    
class HellowWorldGTK:

    def __init__(self):
        self.builder = gtk.Builder()
        self.builder.add_from_file("work.glade")
#        halcomp = hal.component("work")
        self.builder.connect_signals(self)
        self.window = self.builder.get_object("MainWindow")
        self.window.show()
#        panel = gladevcp.makepins.GladePanel( halcomp, "work.glade", self.builder, None)
 #       halcomp.ready()
        
#         
#         self.gladefile = "face1.glade" 
#         self.glade = gtk.Builder()
#         self.glade.add_from_file(self.gladefile)
#         halcomp = hal.component("face1")
#         self.glade.connect_signals(self)
#         self.glade.get_object("MainWindow").show_all()

    def on_MainWindow_delete_event(self, widget, event):
        gtk.main_quit()
        
    def gtk_widget_destroy(self, widget, event):
        gtk.main_quit()  
    
    def on_notebook1_select_page(self, notebook, arg1, user_data):
        print(notebook)  
    
    
        
    def master_page(self, widget):
        self.notebook = self.glade.get_object("notebook1")
        self.notebook.set_current_page(0)
#        self.notebook.set_current_page(self.notebook.get_current_page()+1)
    def change_page_down(self, widget):
        self.notebook = self.glade.get_object("notebook1")
        self.notebook.prev_page()
#        self.notebook.set_current_page(self.notebook.get_current_page()-1)   
    
    def helloWorld(self, widget):
        
        gtk.main_quit()
#         print(self)
#         print(widget)
#         self.glade.get_object("label1").set_text('Ебана в рот')
        

if __name__ == "__main__":
    hwg = HellowWorldGTK()
    gtk.main()    
