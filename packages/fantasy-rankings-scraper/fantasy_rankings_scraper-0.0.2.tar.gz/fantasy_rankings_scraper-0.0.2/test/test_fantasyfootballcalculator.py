import unittest
from fantasy_rankings_scraper import scrape


class TestFantasyFootballCalculatorScraper(unittest.TestCase):
    def test_scrape_rankings(self):
        scraper = scrape("fantasyfootballcalculator.com")
        self.assertGreaterEqual(len(scraper.half_ppr_rankings()), 1)
        self.assertGreaterEqual(len(scraper.get_format(1)), 1)
