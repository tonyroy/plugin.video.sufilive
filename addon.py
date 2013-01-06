from xbmcswift2 import Plugin
import re
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup as BS

BASE_URL = 'http://www.sufilive.com'
plugin = Plugin()


@plugin.route('/')
def index():
    items = [
            { 'label': 'Latest Sohbet','path': plugin.url_for('list_media', category='Latest', page_no='1')},
            { 'label': 'Categories','path': plugin.url_for('show_categories')},

    ] 
    return items

@plugin.route('/Categories/')
def show_categories():
    html = _html(BASE_URL)
    links = html.findAll('a',href=re.compile('.*-\d*-g.html'))
    items = [{
        'label': unicode(link.string),
        'path' : plugin.url_for('list_media',category=unicode(link.string), page_no='1',url=link['href']),
    } for link in links]                               
    return items


@plugin.route('/List/<category>/<page_no>/')
def list_media(category='',page_no='1'):
    plugin.log.debug('page_no =  %s' % page_no)
    if 'url' in plugin.request.args:
        url = plugin.request.args['url'][0]
        plugin.log.debug('url =  %s' % url)
    else :
        url = 'index.cfm'
    pager = "?p=%d" % int(page_no)
    full_url = _url(url + pager)
    plugin.log.debug('getting %s' % full_url)
    html = _html(full_url)
    nodes = html.findAll('table',attrs={'background':'/img/titleBg.jpg'})

    items = [{
        'label': unicode(node.find('a', attrs={'class':'mediaTitle'}).string),
        'path' : plugin.url_for('play_sohbet',url=node.table.a['href']),
        'icon' : _url(node.img['src']),
        'is_playable': True,
        
    } for node in nodes]
    
    if html.find('a', text=re.compile(r'.*Next.*')) :
        next_page = str(int(page_no)+1 )
        plugin.log.debug('next page is  %s' % next_page)
        next_link = plugin.url_for('list_media',category=category,page_no=next_page, url=url),
        items.append ({
            'label' : 'Next (page %s )' % next_page,
            'path'   : plugin.url_for('list_media',category=category,page_no=next_page, url=url),
            'is_playable' : False,
        })
    else :
        plugin.log.debug('no next page')
    return items


@plugin.route('/Play/<url>/')
def play_sohbet(url):
    url = _url(url)
    plugin.log.debug('video hosted at url : %s ' % url)
    html = _html(url)
    link = html.find('iframe',src=re.compile(".*youtube.*"))
    if link :
        url = link['src']

        plugin.log.debug('youtube source : %s' % url)
        youTubeId = url.split('/')[-1]
        plugin.log.debug('youtube id : %s' % youTubeId)
        
        url ='plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youTubeId 
        plugin.set_resolved_url(url)
    else :
        link = html.find('a', href=re.compile('.*(mp4|flv)$'))
        if link :
            
            plugin.log.debug('direct source : %s' % link['href'])
            plugin.set_resolved_url(link['href'])
        else:
            plugin.log.debug('unable to determine source : %s' % html)

    pass

def _url(path):
    '''Returns a full url for the given path'''
    return urlparse.urljoin(BASE_URL, path)


def get(url):
    '''Performs a GET request for the given url and returns the response'''
    headers = {'user+agent': 'Mozilla/5 (Solaris10) gecko'}

    req = urllib2.Request(url,None,headers)
    resp = urllib2.urlopen(req)
    got = resp.read()
    return got


def _html(url):
    '''Downloads the resource at the given url and parses via BeautifulSoup'''
    return BS(get(url))


    
if __name__ == '__main__':
    plugin.run()
