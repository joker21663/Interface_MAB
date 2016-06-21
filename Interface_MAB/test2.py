#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gtk        

class TestWindow:
    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        box = gtk.VBox()

        button0 = gtk.Button("Test Button")
        label0 = button0.get_children()[0]
        label0.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('red'))

        button1 = gtk.Button(stock=gtk.STOCK_ABOUT)
        alignment = button1.get_children()[0]
        hbox = alignment.get_children()[0]
        image, label1 = hbox.get_children()
        label1.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse('blue'))

        box.add(button0)
        box.add(button1)

        window.add(box)
        window.set_size_request(200, 200)
        window.show_all()        

    def close_application(self, widget, event, data=None):
        gtk.main_quit()
        return False

if __name__ == "__main__":
    TestWindow()
    gtk.main()