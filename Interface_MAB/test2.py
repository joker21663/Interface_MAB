from gscreen import mdi
import pprint

class Greeter:

  def __init__(self):

    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    self.box = gtk.VBox()
    self.window.add(self.box)

    self.label = gtk.Label("Please enter your name in the box below:")
    self.namebox = gtk.Entry(12)
    self.button = gtk.Button("Greet Me!")
    self.output = gtk.Label("Your output will appear here.")

    self.box.pack_start(self.label, False, False, 2)
    self.box.pack_start(self.namebox, False, False, 2)
    self.box.pack_start(self.button, False, False, 2)
    self.box.pack_start(self.output, False, False, 2)

    self.label.show()
    self.namebox.show()
    self.button.show()
    self.output.show()
    self.box.show()
    self.window.show()

  def main(self):
    pprint(mdi)
    gtk.main()

    a = Greeter()
    a.main()
