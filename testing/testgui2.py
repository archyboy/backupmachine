import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk





class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello World")
        self.mystring = "Starting game!!"
        self.button = Gtk.Button(label="Start game")
        self.button.connect("clicked", self.continueGame)
        self.add(self.button)

    def continueGame(self, widget):
        print(self.mystring)
        print(list(widget.props))

    def startGui():
        win = MyWindow()
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()

MyWindow.startGui()
