# Music Play Bot 🎵

A Telegram bot that downloads music files from users and plays them on a Linux system.

## Features

- 📥 Download audio files sent by users via Telegram
- 🎵 Play downloaded music on the Linux system
- 🎮 Control playback with commands (/play, /stop, /pause, /resume)
- 📋 List available downloaded tracks
- 🎚️ Volume control
- 📊 Storage management
- 🎼 Audio metadata display

## Quick Setup

1. **Automated Setup (Recommended)**:
   ```bash
   ./setup.sh
   ```

2. **Manual Setup**:
   
   a. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install -y python3-pip python3-dev portaudio19-dev libasound2-dev
   ```
   
   b. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   c. Create configuration:
   ```bash
   cp .env.example .env
   ```

3. **Get a Telegram Bot Token**:
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Create a new bot with `/newbot`
   - Copy the token to your `.env` file

4. **Configure SOCKS5 Proxy (Optional)**:
   
   If you need to use a SOCKS5 proxy, edit your `.env` file:
   ```bash
   # For proxy with authentication
   SOCKS5_PROXY_URL=socks5://username:password@proxy_host:1080
   
   # For proxy without authentication
   SOCKS5_PROXY_URL=socks5://127.0.0.1:1080
   ```

5. **Run the bot**:
   ```bash
   python main.py
   ```

## Commands

- `/start` - Start the bot and show help
- `/play [track_name]` - Play a specific track or resume playback
- `/stop` - Stop current playback
- `/pause` - Pause current playback
- `/resume` - Resume paused playback
- `/list` - List all downloaded tracks
- `/current` - Show current playing track
- `/help` - Show available commands

## Usage

1. Send an audio file to the bot
2. The bot will download and save it
3. Use `/list` to see available tracks
4. Use `/play track_name` to play a specific track

## Requirements

- Linux system with audio output
- Python 3.8+
- Telegram Bot Token