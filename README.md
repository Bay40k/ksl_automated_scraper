# ksl_automated_scraper

Automatically send an email including KSL Classifieds search results for a specified query, matching a price range.

This only works on the Classifieds section. For https://cars.ksl.com, see: https://github.com/Bay40k/ksl_cars_scraper_api


### Dependencies:
- BeautifulSoup4
- Requests

## Usage:
First, make sure to rename `config_EXAMPLE.py` to `config.py` after configuring your settings.

Then:
```commandline
git clone https://github.com/Bay40k/ksl_automated_scraper
python ksl_automated_scraper
```

## Scheduling:

Cron job which runs scrape every 12 hours
```bash
0 */12 * * * python ~/ksl_automated_scraper/automated_scrape_email.py
```


Or create a scheduled task in Windows: https://www.askpython.com/python/examples/execute-python-windows-task-scheduler
