#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, gobject


def wrap(widget):
    sw = gtk.ScrolledWindow()
    sw.add(widget)
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
    sw.set_border_width(1)
    return sw


def on_selection_changed(selection, textview):
    def grab_this(textview):
        textview.grab_focus()
        return False
    gobject.idle_add(grab_this, textview)
    return False


if __name__ == "__main__":
    paned = gtk.HPaned()

    treestore = gtk.TreeStore(str)

    new_iter = treestore.append(None)
    treestore.set(new_iter, 0, '00000')
    new_iter = treestore.append(None)
    treestore.set(new_iter, 0, '11111')
    new_iter = treestore.append(None)
    treestore.set(new_iter, 0, '22222')
    new_iter = treestore.append(None)
    treestore.set(new_iter, 0, '33333')
    new_iter = treestore.append(None)
    treestore.set(new_iter, 0, '44444')

    treeview = gtk.TreeView(treestore)
    treeview.set_enable_search(False)

    column = gtk.TreeViewColumn();
    renderer = gtk.CellRendererText()
    column.pack_start(renderer, False)
    column.add_attribute(renderer, 'text', 0)
    treeview.append_column(column)

    paned.add1(wrap(treeview))

    textview = gtk.TextView()
    paned.add2(wrap(textview))
    paned.set_position(250)

    treeview.get_selection().connect_after('changed', on_selection_changed,
textview)

    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_default_size(800, 600)
    window.add(paned)
    window.show_all()

    gtk.main()