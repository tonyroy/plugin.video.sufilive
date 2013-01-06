#!/usr/bin/env python
import sys,os
import unittest
sys.path.insert(0,os.path.join(os.path.dirname(__file__),'../lib'))
from sufilive import SufiLiveScraper
class testScraper(unittest.TestCase):
    
    def test_get_youtubId(self):
        known_values = [
            ('http://www.youtube.com/embed/Vn1uXtE2saI','Vn1uXtE2saI' )
        ]
        scraper = SufiLiveScraper()
        for inp,expected in known_values:
            self.assertEqual(scraper.get_youube_id(inp), expected)
            
    def test_get_stuff(self):
        scraper = SufiLiveScraper()
if __name__ == '__main__':
    unittest.main()
