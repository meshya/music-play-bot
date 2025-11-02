"""
Audio player module for the Music Play Bot.
Handles audio playback using pygame mixer.
"""

import pygame
import os
import threading
from typing import Optional, List
from mutagen import File as MutagenFile
from .config import config

class AudioPlayer:
    """Audio player class to manage music playback."""
    
    def __init__(self):
        # Initialize pygame mixer
        pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=config.audio_buffer_size)
        pygame.mixer.init()
        
        # Player state
        self.current_track: Optional[str] = None
        self.is_playing: bool = False
        self.is_paused: bool = False
        self.volume: float = config.default_volume
        self.playlist: List[str] = []
        self.current_index: int = 0
        
        # Set initial volume
        pygame.mixer.music.set_volume(self.volume)
    
    def load_track(self, file_path: str) -> bool:
        """Load an audio track for playback."""
        if not os.path.exists(file_path):
            print(f"Audio file not found: {file_path}")
            return False
        
        try:
            pygame.mixer.music.load(file_path)
            self.current_track = file_path
            return True
        except pygame.error as e:
            print(f"Error loading audio file: {e}")
            return False
    
    def play(self, file_path: Optional[str] = None) -> bool:
        """Play an audio track."""
        if file_path:
            if not self.load_track(file_path):
                return False
        
        if not self.current_track:
            print("No track loaded")
            return False
        
        try:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.play()
            
            self.is_playing = True
            return True
        except pygame.error as e:
            print(f"Error playing audio: {e}")
            return False
    
    def stop(self):
        """Stop audio playback."""
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
    
    def pause(self):
        """Pause audio playback."""
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
    
    def resume(self):
        """Resume paused audio playback."""
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
    
    def set_volume(self, volume: float):
        """Set playback volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)
    
    def is_busy(self) -> bool:
        """Check if music is currently playing."""
        return pygame.mixer.music.get_busy()
    
    def get_track_info(self, file_path: str) -> dict:
        """Get metadata information about an audio track."""
        try:
            audio_file = MutagenFile(file_path)
            if audio_file is None:
                return {"title": os.path.basename(file_path), "artist": "Unknown", "duration": "Unknown"}
            
            title = audio_file.get("TIT2", [os.path.basename(file_path)])[0] if "TIT2" in audio_file else os.path.basename(file_path)
            artist = audio_file.get("TPE1", ["Unknown"])[0] if "TPE1" in audio_file else "Unknown"
            
            # Get duration in seconds
            duration = getattr(audio_file.info, 'length', 0)
            duration_str = f"{int(duration // 60):02d}:{int(duration % 60):02d}" if duration else "Unknown"
            
            return {
                "title": str(title),
                "artist": str(artist),
                "duration": duration_str,
                "file_size": os.path.getsize(file_path)
            }
        except Exception as e:
            print(f"Error reading track metadata: {e}")
            return {"title": os.path.basename(file_path), "artist": "Unknown", "duration": "Unknown"}
    
    def get_status(self) -> dict:
        """Get current player status."""
        return {
            "current_track": os.path.basename(self.current_track) if self.current_track else None,
            "is_playing": self.is_playing,
            "is_paused": self.is_paused,
            "volume": self.volume,
            "is_busy": self.is_busy()
        }

# Create global audio player instance
audio_player = AudioPlayer()