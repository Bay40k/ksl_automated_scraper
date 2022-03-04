config_options = {
    "settings": {
        # Keyword to search for
        "keyword": "ps5",
        "price_from": 450,
        "price_to": 600,
        # Integer, optional zip code for miles radius
        "zip_code": None,
        # Integer, miles radius for zip code, will default to 0 if None and zip_code is not None
        # Will also default to 0 if value not in: [0, 10, 25, 50, 100, 150, 200], or 10000 if value over 200
        "miles_radius": None,
    },
    "email": {
        # To use Gmail, generate an App Password: https://support.google.com/accounts/answer/185833
        # use SSL server, not TLS
        "mail_server": "smtp.gmail.com",
        "mail_port": 465,
        "email_from": "",
        "email_password": "",
        "email_to": "",
    },
    "discord": {
        # Discord bot token if using Discord, see: https://docs.pycord.dev/en/master/discord.html
        "discord_token": "",
        # Your Discord user ID (for sending the notification)
        "discord_user_id": 0,
    },
    "proxy": {
        # Optional SOCKS5 proxy settings to use for the requests
        "username": "",
        "password": "",
        "url": "",
        "port": 0,
    },
    "database": {
        # Path to already-sent-links database, absolute path needed or else cron won't work
        "db_location": "already_sent.db",
    },
}
