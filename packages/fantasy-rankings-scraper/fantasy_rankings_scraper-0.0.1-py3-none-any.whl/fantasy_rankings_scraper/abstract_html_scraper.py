HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}


class AbstractHTMLScraper:
    def __init__(self, site: str, ppr_scoring: float = 0.0) -> None:
        self.headers = HEADERS
        pass

    @classmethod
    def host(cls):
        pass

    def ppr_scoring(self):
        pass

    def player_count(self):
        pass

    def result(self):
        pass
