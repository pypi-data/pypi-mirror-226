# FANTASY-RANKINGS-SCRAPER [![n-roth12](https://circleci.com/gh/n-roth12/fantasy-rankings-scraper.svg?style=shield)](https://app.circleci.com/pipelines/github/n-roth12/fantasy-rankings-scraper)
A Python package for scraping fantasy football draft rankings across multiple websites.

### Installation
#### Repo
Clone the repository onto your machine to get started. Ensure you have Python and pip installed, then set up the virtual environment using:
```
pipenv install -r "requirements.txt"
pipenv shell
```
### Usage
#### Command Line Example
```
python scrape.py fantasypros.com 1
```
These will output the scraped Standard scoring rankings from fantasypros.com. 
### About 
#### Scoring Format Mapping
* 1 = Standard
* 2 = Half-PPR
* 3 = PPR
#### Currently Supported Sites
* [FantasyFootballCalculator](https://fantasyfootballcalculator.com/)   
* [Rotoballer](https://www.rotoballer.com/)   
* [FantasyPros](https://www.fantasypros.com/)
#### Terms
This project is for learning purposes only. Scraping websites may violate terms of use. Please use responsibly and do not create large volumes of traffic for supported sites. This project is in no way affiliated with the NFL or any of the supported websites.
