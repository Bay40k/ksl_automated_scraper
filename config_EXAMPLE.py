config_options = {
    "settings": {
        # Keyword to search for
        "keyword": "ps5",
        "price_from": 450,
        "price_to": 600,
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
    "proxy":
    # Optional proxy settings to use for the requests
    {"username": "", "password": "", "url": "", "port": 0},
}
