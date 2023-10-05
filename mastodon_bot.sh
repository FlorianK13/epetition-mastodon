#!/bin/bash
LOG_FILE="/home/flo/mastobot/mastodon_bot.log"
cd mastobot && /home/flo/miniconda3/envs/mastobot/bin/python mastodon_bot.py >> "$LOG_FILE" 2>&1
