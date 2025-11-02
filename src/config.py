"""
Configuration module for the Music Play Bot.
Loads settings from environment variables and .env file.
"""

import os
from dotenv import load_dotenv
from typing import List
from pathlib import Path

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent/'.env')

class Config:
    """Configuration class to manage bot settings."""
    
    def __init__(self):
        self.telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.download_path = os.getenv('DOWNLOAD_PATH', './downloads')
        self.max_file_size_mb = int(os.getenv('MAX_FILE_SIZE_MB', 50))
        self.allowed_extensions = self._parse_extensions(os.getenv('ALLOWED_EXTENSIONS', 'mp3,wav,ogg,m4a,flac'))
        self.default_volume = float(os.getenv('DEFAULT_VOLUME', 0.7))
        self.audio_buffer_size = int(os.getenv('AUDIO_BUFFER_SIZE', 1024))
        
        # Proxy settings
        self.socks5_proxy_url = os.getenv('SOCKS5_PROXY_URL', '').strip()
        
        # Validate critical settings
        self._validate_config()
    
    def _parse_extensions(self, extensions_str: str) -> List[str]:
        """Parse allowed file extensions from comma-separated string."""
        return [ext.strip().lower() for ext in extensions_str.split(',')]
    
    def _validate_config(self):
        """Validate critical configuration settings."""
        if not self.telegram_bot_token or self.telegram_bot_token == 'your_bot_token_here':
            raise ValueError("TELEGRAM_BOT_TOKEN is not set in .env file. Please get a token from @BotFather on Telegram.")
        
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path, exist_ok=True)
            print(f"Created download directory: {self.download_path}")
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size from MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024
    
    def is_allowed_extension(self, filename: str) -> bool:
        """Check if a file has an allowed extension."""
        if '.' not in filename:
            return False
        extension = filename.split('.')[-1].lower()
        return extension in self.allowed_extensions
    
    def get_proxy_config(self) -> dict:
        """Get proxy configuration for httpx/telegram bot."""
        if not self.socks5_proxy_url:
            return {}
        
        return {
            "proxies": {
                "http://": self.socks5_proxy_url,
                "https://": self.socks5_proxy_url
            }
        }
    
    def has_proxy(self) -> bool:
        """Check if proxy is configured."""
        return bool(self.socks5_proxy_url)

# Create global config instance
config = Config()