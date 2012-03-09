# -*- coding: utf-8 -*-

import os
import Image
import urllib
import urllib2
import ImageDraw
import ImageFont
from BeautifulSoup import BeautifulSoup

# period:  overall | 7day | 3month | 6month | 12mont
URL = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=%s&api_key=%s&period=%s&limit=10'
API_KEY = '344245cb8610e8490d7abd82c980d191'
IMAGE_TEMP_PATH = '/tmp/'
FONT_RANK = ImageFont.truetype("/home/%s/.local/share/rhythmbox/plugins/top10/fonts/UnBatang.ttf" % os.getlogin(), 25)
FONT_INFO = ImageFont.truetype("/home/%s/.local/share/rhythmbox/plugins/top10/fonts/UnBatang.ttf" % os.getlogin(), 12)
FONT_ARTIST = ImageFont.truetype("/home/%s/.local/share/rhythmbox/plugins/top10/fonts/UnBatang.ttf" % os.getlogin(), 16)


def do_top10_image(nick, period):
    BACKGROUND = Image.open('/home/%s/.local/share/rhythmbox/plugins/top10/images/compound.jpeg' % os.getlogin()) 
    DRAW = ImageDraw.Draw(BACKGROUND)

    request = urllib2.Request(URL % (nick, API_KEY, period))
    response = urllib2.urlopen(request)

    document = response.read()
    soup = BeautifulSoup(document)

    for t_art in enumerate(soup.findAll('artist')):
        # rank
        t_art[1].attrs[0][1]
        # name of artist
        artist_name = t_art[1].find('name').text
        # playcount into period
        playcount = t_art[1].find('playcount').text 
        # large image to put on list image 
        image = t_art[1].findAll('image')[2].text 

        artist_name =  artist_name[0]+artist_name[1:].lower()

        if len(artist_name) > 15:
            reticences  = "..."
            artist_name = artist_name[:15]
        else:
            reticences = ''

        # compouding image...   
        # way one
        # file_image = open(IMAGE_TEMP_PATH+'temp.jpeg','wb') 
        # file_image.write(urllib.urlopen(image).read())
        # file_image.close()
        
        # way two
        urllib.urlretrieve(image, "/tmp/temp.jpeg")

        temp = Image.open('/tmp/temp.jpeg')
        temp = temp.resize((50,50), Image.ANTIALIAS)
        BACKGROUND.paste(temp,(230,t_art[0] * (temp.size[0])+20))
        DRAW.text((45, 3), "%s's top 10 artist (%s)" % (nick,period), \
            fill=(0,0,0))#, font=FONT_INFO)
        DRAW.text((10,t_art[0] * (temp.size[0]) + 30), str(t_art[0]+1)+'.', \
            fill=(255,0,0), font=FONT_RANK)
        DRAW.text((45, t_art[0]* (temp.size[0]) +37), artist_name+' '+
            reticences+'('+playcount+')', fill=(255,0,0), font=FONT_ARTIST)
        
    BACKGROUND.save("/tmp/top10.jpeg")

