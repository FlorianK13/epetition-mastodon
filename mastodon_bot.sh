#!/bin/bash
LOG_FILE="mastodon_bot.log"
python mastodon_bot.py >> "$LOG_FILE" 2>&1
