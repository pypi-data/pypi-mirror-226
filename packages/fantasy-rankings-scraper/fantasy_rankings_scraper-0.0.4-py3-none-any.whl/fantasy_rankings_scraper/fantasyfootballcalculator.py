from bs4 import BeautifulSoup
import requests
from .abstract_scraper import AbstractScraper
from .format import Format

URLS = {
    Format.STANDARD:
        "https://fantasyfootballcalculator.com/rankings/standard",
    Format.HALF_PPR:
        "https://fantasyfootballcalculator.com/rankings/half-ppr",
    Format.PPR:
        "https://fantasyfootballcalculator.com/rankings/ppr"
}


class FantasyFootballCalculatorScraper(AbstractScraper):
    @classmethod
    def host(cls):
        return "fantasyfootballcalculator.com"

    @classmethod
    def supported_formats(cls) -> list:
        return [format.name for format in URLS.keys()]

    def __init__(self) -> None:
        super().__init__()
        for format in URLS.keys():
            self.data[format] = self.scrape(format)

    def scrape(self, format: str):
        results = requests.get(URLS[format], headers=self.headers, timeout=5)
        soup = BeautifulSoup(results.text, "html.parser")

        table = soup.find("table")
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")
        result = []

        for tr in trs:
            tds = tr.find_all("td")
            result.append({
                "rank": int(tds[0].text.replace(".", "")),
                "name": tds[1].find("a").text,
                "team": tds[2].text,
                "position": tds[3].text,
                "bye": int(tds[4].text)
            })

        return result
    
    def get_format(self, format: str):
        if format not in self.data.keys():
            print('Error: Invalid format provided')
            return None
        return self.data[format]

    def standard_rankings(self):
        return self.data[Format.STANDARD]

    def half_ppr_rankings(self):
        return self.data[Format.HALF_PPR]

    def ppr_rankings(self):
        return self.data[Format.PPR]
