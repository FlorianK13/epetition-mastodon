# epetition-mastodon
Source code for the bot [Bundestagpetition 10k](https://troet.cafe/@bundestagpetitionen10k).

The `mastodon_bot.py` runs once per day on a server to fetch the current petitions ordered by the amount of supporters. 
If a petition has more than 10k supporters and if it was not already posted, it will be posted on mastodon once.
