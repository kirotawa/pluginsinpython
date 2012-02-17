# -*- coding: utf-8 -*-

import os
from gi.repository import GdkPixbuf, GObject, Gio, RB, Peas, Gtk, Gdk
from Top10ConfigureDialog import Top10ConfigureDialog, IMAGE_DEFAULT_PATH, IMAGE_PATH



class Top10Plugin(GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.GObject)
    

    def __init__(self):
        super(Top10Plugin, self).__init__()
        self._settings = Gio.Settings("rhythmbox.plugin.top10")    
        if not os.path.exists(IMAGE_PATH):
            self._settings['imagepath'] = IMAGE_DEFAULT_PATH

    def do_activate(self):
        shell = self.object
        self.image = Gtk.Image()

        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file (self._settings['imagepath'])
        self.image.set_from_pixbuf(self.pixbuf)

        self.container = Gtk.VBox ()
        self.container.pack_start (self.image, True, True, 6)
        
        shell.add_widget(self.container, RB.ShellUILocation.RIGHT_SIDEBAR, False, True)
        self.container.show_all()

    def do_deactivate(self):
        shell = self.object
        shell.remove_widget(self.container, RB.ShellUILocation.RIGHT_SIDEBAR) 
        self.image = None
        self.pixbuf = None
        self.container = None

