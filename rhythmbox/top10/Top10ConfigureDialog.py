# -*- coding: utf-8 -*-

import rb
import os
# import urllib 
# import urllib2
from threading import Thread    
# from BeautifulSoup import BeautifulSoup
from gi.repository import GdkPixbuf, RB, Gtk, Gio, GObject, PeasGtk
from topimagegenerate import do_top10_image 

IMAGE_PATH = "/tmp/top10.jpeg"
IMAGE_LOAD_PATH = "/home/%s/.local/share/rhythmbox/plugins/top10/images/loading.gif" % os.getlogin()
IMAGE_DEFAULT_PATH = "/home/%s/.local/share/rhythmbox/plugins/top10/images/default.jpeg" % os.getlogin()


class Load(Thread):
    ''' Class load and make the low level that is necessary '''

    def __init__(self, user, period, img_load):
        Thread.__init__(self) 
        self.nick = user
        self.period = period
        self.img = img_load

    def run(self):
        try:
           do_top10_image(self.nick, self.period) 

        except:
            pass
    
        self.img.hide() 


class Top10ConfigureDialog (GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'Top10ConfigureDialog'
    object = GObject.property(type=GObject.Object)
    
    period_dic = {0:"overall", 1:'7day', 2:'3month', 3:'6month', 4:'12month'}

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings("rhythmbox.plugin.top10")

    def do_activate(self):
        pass

    def do_create_configure_widget(self):
        builder = Gtk.Builder()
        builder.add_from_file(rb.find_plugin_file(self,"configure.ui"))
            
        self.box1 = builder.get_object("box1")
        self.config = builder.get_object("fixed1")
        self.nick = builder.get_object("lastfm_nick")
        self.combo = builder.get_object("Period")
        self.combo.connect("changed", self.callback)

        return self.config

    def callback(self, widget):
        self.settings['period'] = self.period_dic[self.combo.get_active()]
        if self.nick.get_text() != '':
            self.settings['lastfmuser'] = self.nick.get_text()  
         
        self.image = Gtk.Image()
        load_image = Load(self.settings['lastfmuser'], self.settings['period'], self.image)
        
        self.animation = GdkPixbuf.PixbufAnimation.new_from_file(IMAGE_LOAD_PATH)
        self.image.set_from_animation(self.animation) 
        self.box1.add(self.image)
        self.image.show()
        load_image.start()
        self.settings['imagepath'] = IMAGE_PATH

    def do_deactivate(self):
        pass        

