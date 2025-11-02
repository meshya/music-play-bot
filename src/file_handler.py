"""
File handler module for the Music Play Bot.
Manages file downloads and storage.
"""

import os
import asyncio
from typing import List, Optional
from telegram import Update, File
from .config import config

class FileHandler:
    """File handler class to manage audio file downloads and storage."""
    
    def __init__(self):
        self.download_path = config.download_path
        # Ensure download directory exists
        os.makedirs(self.download_path, exist_ok=True)
    
    async def download_audio_file(self, file: File, original_filename: str) -> Optional[str]:
        """Download an audio file from Telegram."""
        try:
            # Validate file size
            if file.file_size > config.max_file_size_bytes:
                raise ValueError(f"File too large. Maximum size is {config.max_file_size_mb}MB")
            
            # Validate file extension
            if not config.is_allowed_extension(original_filename):
                raise ValueError(f"File type not supported. Allowed types: {', '.join(config.allowed_extensions)}")
            
            # Generate safe filename
            safe_filename = self._generate_safe_filename(original_filename)
            file_path = os.path.join(self.download_path, safe_filename)
            
            # Download the file
            await file.download_to_drive(file_path)
            
            print(f"Downloaded: {safe_filename} ({file.file_size} bytes)")
            return file_path
            
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None
    
    def _generate_safe_filename(self, filename: str) -> str:
        """Generate a safe filename, handling duplicates."""
        # Remove unsafe characters
        safe_chars = []
        for char in filename:
            if char.isalnum() or char in '.-_':
                safe_chars.append(char)
            else:
                safe_chars.append('_')
        safe_filename = ''.join(safe_chars)
        
        # Handle duplicates
        base_name, extension = os.path.splitext(safe_filename)
        counter = 1
        final_filename = safe_filename
        
        while os.path.exists(os.path.join(self.download_path, final_filename)):
            final_filename = f"{base_name}_{counter}{extension}"
            counter += 1
        
        return final_filename
    
    def list_audio_files(self) -> List[dict]:
        """List all downloaded audio files."""
        audio_files = []
        
        for filename in os.listdir(self.download_path):
            if config.is_allowed_extension(filename):
                file_path = os.path.join(self.download_path, filename)
                file_size = os.path.getsize(file_path)
                
                audio_files.append({
                    'filename': filename,
                    'path': file_path,
                    'size': file_size,
                    'size_mb': round(file_size / (1024 * 1024), 2)
                })
        
        # Sort by filename
        return sorted(audio_files, key=lambda x: x['filename'])
    
    def find_audio_file(self, search_term: str) -> Optional[str]:
        """Find an audio file by partial name match."""
        search_term = search_term.lower()
        
        for filename in os.listdir(self.download_path):
            if config.is_allowed_extension(filename) and search_term in filename.lower():
                return os.path.join(self.download_path, filename)
        
        return None
    
    def delete_audio_file(self, filename: str) -> bool:
        """Delete an audio file."""
        file_path = os.path.join(self.download_path, filename)
        
        if os.path.exists(file_path) and config.is_allowed_extension(filename):
            try:
                os.remove(file_path)
                print(f"Deleted: {filename}")
                return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
        
        return False
    
    def get_storage_info(self) -> dict:
        """Get information about storage usage."""
        files = self.list_audio_files()
        total_files = len(files)
        total_size = sum(file_info['size'] for file_info in files)
        total_size_mb = round(total_size / (1024 * 1024), 2)
        
        return {
            'total_files': total_files,
            'total_size_bytes': total_size,
            'total_size_mb': total_size_mb,
            'download_path': self.download_path
        }

# Create global file handler instance
file_handler = FileHandler()