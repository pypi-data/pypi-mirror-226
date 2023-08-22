import sys
from fantasy_rankings_scraper import scrape
from fantasy_rankings_scraper.format import Format


def scrape_rankings(args: list):
    if len(args) < 3:
        print('Missin arguments: must include both site and player pool filename.')
        return
    site = args[1]
    format = args[2]

    rankings = scrape(site)
    print(rankings.get_format(Format(int(format))))


if __name__ == '__main__':
    scrape_rankings(sys.argv)
