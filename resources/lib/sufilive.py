import re
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup as BS

BASE_URL = 'http://www.sufilive.com'

def _url(path):
    '''Returns a full url for the given path'''
    return urlparse.urljoin(BASE_URL, path)


def get(url):
    '''Performs a GET request for the given url and returns the response'''
    headers = {'user+agent': 'xbmc/2'}
    req = urllib2.Request(url,None,headers)
    resp = urllib2.urlopen(req)
    got = resp.read()
    return got


def _html(url):
    '''Downloads the resource at the given url and parses via BeautifulSoup'''
    return BS(get(url))

class SufiLiveScraper(object) :
        
    def get_categories(self):
        html = _html(BASE_URL)
        links = html.findAll('a',href=re.compile('.*-\d*-g.html'))
        items = [{
            'label': unicode(link.string),
            'path' : link['href'],
        } for link in links]                               
        return items
    
    
    def list_media(self,category='',page_no=1,url='index.cfm'):
        pager = "?p=%d" % page_no
        full_url = _url(url + pager)
        html = _html(full_url)
        nodes = html.findAll('table',attrs={'background':'/img/titleBg.jpg'})
    
        items = [{
            'label': unicode(node.find('a', attrs={'class':'mediaTitle'}).string),
            'path' : node.table.a['href'],
            'icon' : _url(node.img['src']),
            
        } for node in nodes]
        
        if html.find('a', text=re.compile(r'.*Next.*')) :
            next_page = page_no+1 
        else :
            next_page = None
        return ({'items': items, 'next_page': next_page})
    
    
    def get_media_link(self, url):
        html = _html(_url(url))
        link = html.find('iframe',src=re.compile(".*youtube.*"))
        if link :
            youTubeId = self.get_youtube_id(link['src'])
            url ='plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youTubeId 
            return url
        link = html.find('a', href=re.compile('.*(mp4|flv)$'))
        if link :
            return link['href']
    
    def get_youtube_id(self,url):
        return  url.split('/')[-1]
        

