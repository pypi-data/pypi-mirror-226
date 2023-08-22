from bs4 import BeautifulSoup
import requests
import re
import json
from .abstract_scraper import AbstractScraper
from .format import Format

URLS = {
    Format.STANDARD:
        "https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php",
    Format.HALF_PPR:
        "https://www.fantasypros.com/nfl/rankings/half-point-ppr-cheatsheets.php",
    Format.PPR:
        "https://www.fantasypros.com/nfl/rankings/ppr-cheatsheets.php"
}


class FantasyProsScraper(AbstractScraper):
    @classmethod
    def host(self) -> str:
        return "fantasypros.com"

    @classmethod
    def supported_formats(cls) -> list:
        return [format.name for format in URLS.keys()]

    def __init__(self) -> None:
        super().__init__()
        for format in URLS.keys():
            self.data[format] = self.scrape(format)

    def scrape(self, format: str) -> list:
        results = requests.get(URLS[format], headers=self.headers, timeout=5)
        soup = BeautifulSoup(results.text, "html.parser")

        scripts = soup.find_all("script")
        for script in scripts:
            if (script.string):
                z = re.search("var ecrData = {.*};", script.string)
                if z:
                    temp = z.group(0).replace("var ecrData = ", "").replace(";", "")
                    data = json.loads(temp)
                    return data["players"]

    def get_format(self, format: str):
        if format not in self.data.keys():
            print('Error: Invalid format provided')
            return None
        return self.data[format]

    def standard_rankings(self) -> list:
        return self.data[Format.STANDARD]

    def half_ppr_rankings(self) -> list:
        return self.data[Format.HALF_PPR]

    def ppr_rankings(self) -> list:
        return self.data[Format.PPR]
