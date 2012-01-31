
import os
import urllib 
import urllib2
from BeautifulSoup import BeautifulSoup
from gi.repository import GdkPixbuf, GObject, RB, Peas, Gtk, Gdk
from Top10ConfigureDialog import Top10ConfigureDialog

IMAGE_PATH = "/tmp/top10.jpeg"

class Load(object):
    ''' Class load and make the low level that is necessary '''

    url = "http://lastfm.sivy.net/?do=albumForm-submit"

    values = {
        'nick':'kirotawa','type':2,'period':'3month','count':10, 'align':1, 
        'font':20,'font_zoom':100,'generate':'Generate', 'colortext':'0;0;0',
        'colorbackground':'255;255;255'
    }
    
    def __init__(self):
        
        data = urllib.urlencode(self.values)
        request = urllib2.Request(self.url, data)

        response = urllib2.urlopen(request)
        document = response.read()
        soup = BeautifulSoup(document)

        image = soup.find('textarea').contents[0]
        image = image.split('[img]')[1].split('[/img]')[0]
    
        file_image = open(IMAGE_PATH,'wb')
        file_image.write(urllib.urlopen(image).read())
        file_image.close()


class Top10Plugin(GObject.Object, Peas.Activatable):
    object = GObject.property(type=GObject.GObject)
    

    def __init__(self):
        super(Top10Plugin, self).__init__()
    
        if not os.path.exists(IMAGE_PATH):
            Load()
            

    def do_activate(self):
        shell = self.object
        self.image = Gtk.Image()
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file (IMAGE_PATH)
        self.image.set_from_pixbuf(self.pixbuf) # , 175, 328)

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


