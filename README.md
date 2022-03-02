# ksl_automated_scraper

Automatically send an email or Discord message including KSL Classifieds search results for a specified query, matching a price range.

Already sent links will be kept track of via an SQLite database. If no new results are found, no email/message/notification is sent.

This only works on the Classifieds section. For https://cars.ksl.com, see: [ksl_cars_scraper](https://github.com/Bay40k/ksl_cars_scraper_api)


### Dependencies:
- BeautifulSoup4
- Requests
- PyCord (discord2)
- aiosqlite

## Usage
```
git clone https://github.com/Bay40k/ksl_automated_scraper
cd ksl_automated_scraper
pip install -r requirements.txt
```
After installing, make sure to rename `config_EXAMPLE.py` to `config.py` after configuring your settings.

Then, to run the scrape and send the results to your configured email:
```commandline
python automated_scrape_email
```
Or, if you have configured Discord settings:
```commandline
python automated_scrape_discord
```

## Example Output
![censored_example_small](https://user-images.githubusercontent.com/8551516/156336122-a68c2b10-013f-4d7a-b2fb-6af9096079a5.jpg)


## Discord
1. To use Discord, you must first create a bot account and generate an OAuth URL:
https://docs.pycord.dev/en/master/discord.html

2. Make sure it has "Bot" and "Send messages" permissions, then add it to a server you're in using the OAuth URL you generated above.

3. Then, copy your bot's token and *your account's* [User ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) to `config.py`

4. Simply run/schedule `python automated_scrape_discord`.

## Scheduling

Cron job which runs scrape every 12 hours
```bash
0 */12 * * * python ~/ksl_automated_scraper/automated_scrape_email.py
```
Or, for Discord (if configured):
```bash
0 */12 * * * python ~/ksl_automated_scraper/automated_scrape_discord.py
```

Or create a scheduled task in Windows: https://www.askpython.com/python/examples/execute-python-windows-task-scheduler
