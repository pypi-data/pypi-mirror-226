import requests
from .abstract_scraper import AbstractScraper
from .format import Format

URLS = {
    Format.STANDARD:
        "https://rankings.rotoballer.com:8000/api/players?league=Overall&leagueSize=10&page=1&perPage=300&spreadsheet=standard&twoQb=false",
    Format.HALF_PPR:
        "https://rankings.rotoballer.com:8000/api/players?league=Overall&leagueSize=10&page=1&perPage=300&spreadsheet=half-ppr&twoQb=false",
    Format.PPR:
        "https://rankings.rotoballer.com:8000/api/players?league=Overall&leagueSize=10&page=1&perPage=300&spreadsheet=ppr&twoQb=false"
}


class RotoBallerScraper(AbstractScraper):
    @classmethod
    def host(cls):
        return "rotoballer.com"

    @classmethod
    def supported_formats(cls):
        return [format.name for format in URLS.keys()]

    def __init__(self) -> None:
        super().__init__()
        for format in URLS.keys():
            self.data[format] = self.scrape(format)

    def scrape(self, format):
        res = requests.get(URLS[format])
        players = []
        for player in res.json()["data"]:
            players.append({
                "name": player["player"]["name"],
                "rank": player["rank"],
                "position": player["position"],
            })
        return players

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
