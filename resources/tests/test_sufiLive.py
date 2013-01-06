#!/usr/bin/env python
import sys,os
import unittest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../lib'))
from sufilive import SufiLiveScraper
class testScraper(unittest.TestCase):
    
    def  setUp(self) :
        self.scraper = SufiLiveScraper()
        
    def test_get_youtubId(self):
        known_values = [
            ('http://www.youtube.com/embed/Vn1uXtE2saI','Vn1uXtE2saI' )
        ]
        
        for inp,expected in known_values:
            self.assertEqual(self.scraper.get_youtube_id(inp), expected)
            
    def test_get_some_categories(self):
        cats = self.scraper.get_categories()
        assert len(cats)  > 10
        
    def test_list_mediai_default(self) :
        result = self.scraper.list_media()
        assert len(result['items']) > 10
        assert result['next_page'] == 2
     
    def test_get_media_link_youTube(self) :
        result = self.scraper.get_media_link('-4771.html')
        assert 'youtube' in result
        
        
if __name__ == '__main__':
    unittest.main()
