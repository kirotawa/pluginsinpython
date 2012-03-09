# -*- coding: utf-8 -*-

import Image
import urllib
import urllib2
import ImageDraw
import ImageFont
from BeautifulSoup import BeautifulSoup

# period:  overall | 7day | 3month | 6month | 12mont
URL = 'http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=%s&api_key=%s&period=%s&limit=10'
API_KEY = '344245cb8610e8490d7abd82c980d191'
BACKGROUND = Image.open('images/compound.jpeg') 
IMAGE_TEMP_PATH = '/tmp/'
DRAW = ImageDraw.Draw(BACKGROUND)
FONT_RANK = ImageFont.truetype("/usr/share/fonts/truetype/unfonts/UnBatang.ttf", 25)
FONT_INFO = ImageFont.truetype("/usr/share/fonts/truetype/unfonts/UnBatang.ttf", 12)
FONT_ARTIST = ImageFont.truetype("/usr/share/fonts/truetype/unfonts/UnBatang.ttf", 16)


def do_top10_image(nick, period):

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
        file_image = open(IMAGE_TEMP_PATH+'temp.jpeg','wb') 
        file_image.write(urllib.urlopen(image).read())
        file_image.close()
        
        temp = Image.open('/tmp/temp.jpeg')
        temp = temp.resize((50,50), Image.ANTIALIAS)
        BACKGROUND.paste(temp,(230,t_art[0] * (temp.size[0])+20))
        DRAW.text((45, 3), "%s's top 10 artist (%s)" % (nick,period), fill=(0,0,0))#, font=FONT_INFO)
        DRAW.text((10,t_art[0] * (temp.size[0]) + 30), str(t_art[0]+1)+'.', fill=(255,0,0), font=FONT_RANK)
        DRAW.text((45, t_art[0]* (temp.size[0]) +37), artist_name+' '+reticences+'('+playcount+')', fill=(255,0,0), font=FONT_ARTIST)
        
    BACKGROUND.save("/tmp/top10.jpeg")


if __name__ == "__main__":
    do_top10_image('kirotawa','overall')

