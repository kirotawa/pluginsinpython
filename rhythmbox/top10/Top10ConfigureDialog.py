import rb
from gi.repository import Gtk, Gio, GObject, PeasGtk
    
class Top10ConfigureDialog (GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'Top10ConfigureDialog'
    object = GObject.property(type=GObject.Object)
                    
    def __init__(self):
        GObject.Object.__init__(self)
        # self.settings = Gio.Settings("org.gnome.rhythmbox.plugins.top10")
    
    def do_activate(self):
        print "hi"

    def do_create_configure_widget(self):
        builder = Gtk.Builder()
        builder.add_from_file(rb.find_plugin_file(self,"test_.ui"))

        self.config = builder.get_object("fixed1")
        # self.lastfm_user = builder.get_object("lastfm_user_entry")

        return self.config

        # widget = Gtk.CheckButton("Teste")
        # widget.set_border_width(6)
        return widget

    def do_deactivate(self):
        pass
