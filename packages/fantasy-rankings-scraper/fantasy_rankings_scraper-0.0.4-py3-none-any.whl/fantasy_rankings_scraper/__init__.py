from .abstract_scraper import AbstractScraper
from .cbssports import CBSSportsScraper
from .fantasyfootballcalculator import FantasyFootballCalculatorScraper
from .fantasypros import FantasyProsScraper
from .rotoballer import RotoBallerScraper

SCRAPERS = {
    CBSSportsScraper.host(): CBSSportsScraper,
    FantasyFootballCalculatorScraper.host(): FantasyFootballCalculatorScraper,
    FantasyProsScraper.host(): FantasyProsScraper,
    RotoBallerScraper.host(): RotoBallerScraper
}


def scrape(site: str) -> AbstractScraper:
    scraper = SCRAPERS[site]()
    return scraper


def get_supported_sites() -> list:
    return list(SCRAPERS.keys())


def scraper_exists_for_site(site: str) -> bool:
    return site in get_supported_sites()
