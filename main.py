#!/usr/bin/env python3
"""
Main entry point for the Music Play Bot.
Run this file to start the Telegram bot.
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.bot import bot

if __name__ == "__main__":
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("Make sure you have:")
        print("1. Set TELEGRAM_BOT_TOKEN in .env file")
        print("2. Installed dependencies: pip install -r requirements.txt")
        sys.exit(1)