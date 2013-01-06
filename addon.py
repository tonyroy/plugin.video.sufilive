from xbmcswift2 import Plugin
from resources.lib.sufilive import SufiLiveScraper 

plugin = Plugin()
scraper = SufiLiveScraper()

@plugin.cached_route('/')
def index():
    items = [
        { 'label': 'Latest Sohbet','path': plugin.url_for('list_media', category='Latest', page_no='1')},
        { 'label': 'Categories','path': plugin.url_for('show_categories')},
    ] 
    return items

@plugin.cached_route('/Categories/')
def show_categories():
    links = scraper.get_categories()
    items = [{
        'label': link['label'],
        'path' : plugin.url_for('list_media',category=link['label'], page_no='1',url=link['path']),
    } for link in links]                               
    return items


@plugin.cached_route('/List/<category>/<page_no>/')
def list_media(category='',page_no='1'):
    plugin.log.debug('page_no =  %s' % page_no)
    try :
        url = plugin.request.args['url'][0]
    except:
        url = 'index.cfm'
    
    result = scraper.list_media(category,int(page_no),url)
    items = [{
        'label': link['label'],
        'path' : plugin.url_for('play_sohbet',url=link['path']),
        'icon' : link['icon'],
        'is_playable': True,
        
    } for link in result['items'] ]
    
    if  result['next_page'] :
        next_page = str(result['next_page'] )
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


@plugin.cached_route('/Play/<url>/')
def play_sohbet(url):
    link = scraper.get_media_link(url)
    if link :
        plugin.log.info('playing : %s' % link)
        plugin.set_resolved_url(link)
    else :
        plugin.log.error('unable to determine source : %s' % url)

    
if __name__ == '__main__':
    plugin.run()
