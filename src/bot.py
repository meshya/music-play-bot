"""
Main module for the Music Play Bot.
Telegram bot that downloads and plays music files on Linux.
"""

import asyncio
import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from .config import config
from .file_handler import file_handler
from .audio_player import audio_player

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class MusicPlayBot:
    """Main bot class to handle Telegram interactions."""
    
    def __init__(self):
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        welcome_message = (
            "🎵 Welcome to Music Play Bot! 🎵\n\n"
            "I can download and play music files on your Linux system.\n\n"
            "📤 Send me audio files (MP3, WAV, OGG, M4A, FLAC)\n"
            "🎮 Use commands to control playback:\n\n"
            "/play [name] - Play a track\n"
            "/stop - Stop playback\n"
            "/pause - Pause current track\n"
            "/resume - Resume playback\n"
            "/list - Show all tracks\n"
            "/current - Show current track\n"
            "/help - Show this help\n\n"
            f"📁 Max file size: {config.max_file_size_mb}MB\n"
            f"🎼 Supported formats: {', '.join(config.allowed_extensions).upper()}"
        )
        await update.message.reply_text(welcome_message)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = (
            "🎵 Music Play Bot Commands:\n\n"
            "/start - Start the bot\n"
            "/play [track_name] - Play specific track or resume\n"
            "/stop - Stop current playback\n"
            "/pause - Pause current track\n"
            "/resume - Resume paused track\n"
            "/list - List all downloaded tracks\n"
            "/current - Show current playing track\n"
            "/storage - Show storage information\n"
            "/volume [0-100] - Set volume level\n"
            "/help - Show this help\n\n"
            "📤 Just send me an audio file to download it!"
        )
        await update.message.reply_text(help_text)
    
    async def play_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /play command."""
        try:
            if context.args:
                # Play specific track
                search_term = ' '.join(context.args)
                file_path = file_handler.find_audio_file(search_term)
                
                if not file_path:
                    await update.message.reply_text(f"❌ Track not found: '{search_term}'\nUse /list to see available tracks.")
                    return
                
                success = audio_player.play(file_path)
                if success:
                    track_info = audio_player.get_track_info(file_path)
                    await update.message.reply_text(
                        f"🎵 Now playing:\n"
                        f"🎼 {track_info['title']}\n"
                        f"👤 {track_info['artist']}\n"
                        f"⏱️ {track_info['duration']}"
                    )
                else:
                    await update.message.reply_text("❌ Error playing track.")
            else:
                # Resume or play current track
                if audio_player.is_paused:
                    audio_player.resume()
                    await update.message.reply_text("▶️ Resumed playback")
                elif audio_player.current_track:
                    success = audio_player.play()
                    if success:
                        await update.message.reply_text("▶️ Playing current track")
                    else:
                        await update.message.reply_text("❌ Error playing track")
                else:
                    await update.message.reply_text("❌ No track loaded. Use /play [track_name] or send an audio file first.")
        
        except Exception as e:
            logger.error(f"Error in play command: {e}")
            await update.message.reply_text("❌ Error processing play command.")
    
    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stop command."""
        audio_player.stop()
        await update.message.reply_text("⏹️ Playback stopped")
    
    async def pause_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /pause command."""
        if audio_player.is_playing and not audio_player.is_paused:
            audio_player.pause()
            await update.message.reply_text("⏸️ Playback paused")
        else:
            await update.message.reply_text("❌ No track is currently playing")
    
    async def resume_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /resume command."""
        if audio_player.is_paused:
            audio_player.resume()
            await update.message.reply_text("▶️ Playback resumed")
        else:
            await update.message.reply_text("❌ No track is paused")
    
    async def list_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /list command."""
        files = file_handler.list_audio_files()
        
        if not files:
            await update.message.reply_text("📁 No audio files downloaded yet.\nSend me some music files!")
            return
        
        message = "🎵 Downloaded Tracks:\n\n"
        for i, file_info in enumerate(files, 1):
            message += f"{i}. 🎼 {file_info['filename']}\n   📏 {file_info['size_mb']} MB\n\n"
        
        if len(message) > 4000:  # Telegram message limit
            message = message[:4000] + "\n... (list truncated)"
        
        await update.message.reply_text(message)
    
    async def current_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /current command."""
        status = audio_player.get_status()
        
        if status['current_track']:
            track_info = audio_player.get_track_info(audio_player.current_track)
            state = "Playing" if status['is_playing'] and not status['is_paused'] else "Paused" if status['is_paused'] else "Stopped"
            
            message = (
                f"🎵 Current Track:\n"
                f"🎼 {track_info['title']}\n"
                f"👤 {track_info['artist']}\n"
                f"⏱️ {track_info['duration']}\n"
                f"🎚️ Volume: {int(status['volume'] * 100)}%\n"
                f"▶️ Status: {state}"
            )
        else:
            message = "❌ No track loaded"
        
        await update.message.reply_text(message)
    
    async def storage_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /storage command."""
        storage_info = file_handler.get_storage_info()
        
        message = (
            f"💾 Storage Information:\n\n"
            f"📁 Files: {storage_info['total_files']}\n"
            f"📏 Total Size: {storage_info['total_size_mb']} MB\n"
            f"📂 Location: {storage_info['download_path']}"
        )
        
        await update.message.reply_text(message)
    
    async def volume_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /volume command."""
        if not context.args:
            current_volume = int(audio_player.volume * 100)
            await update.message.reply_text(f"🎚️ Current volume: {current_volume}%\nUsage: /volume [0-100]")
            return
        
        try:
            volume_percent = int(context.args[0])
            if 0 <= volume_percent <= 100:
                volume = volume_percent / 100.0
                audio_player.set_volume(volume)
                await update.message.reply_text(f"🎚️ Volume set to {volume_percent}%")
            else:
                await update.message.reply_text("❌ Volume must be between 0 and 100")
        except ValueError:
            await update.message.reply_text("❌ Invalid volume value. Use a number between 0 and 100")
    
    async def handle_audio_file(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle audio file uploads."""
        try:
            # Get the audio file
            if update.message.audio:
                file = await update.message.audio.get_file()
                filename = update.message.audio.file_name or f"audio_{update.message.audio.file_unique_id}.mp3"
            elif update.message.voice:
                file = await update.message.voice.get_file()
                filename = f"voice_{update.message.voice.file_unique_id}.ogg"
            elif update.message.document and config.is_allowed_extension(update.message.document.file_name):
                file = await update.message.document.get_file()
                filename = update.message.document.file_name
            else:
                await update.message.reply_text("❌ Please send an audio file (MP3, WAV, OGG, M4A, FLAC)")
                return
            
            # Send download status
            status_message = await update.message.reply_text("📥 Downloading audio file...")
            
            # Download the file
            file_path = await file_handler.download_audio_file(file, filename)
            
            if file_path:
                track_info = audio_player.get_track_info(file_path)
                await status_message.edit_text(
                    f"✅ Downloaded successfully!\n\n"
                    f"🎼 {track_info['title']}\n"
                    f"👤 {track_info['artist']}\n"
                    f"⏱️ {track_info['duration']}\n\n"
                    f"Use /play {os.path.basename(file_path).split('.')[0]} to play it!"
                )
            else:
                await status_message.edit_text("❌ Failed to download audio file")
        
        except Exception as e:
            logger.error(f"Error handling audio file: {e}")
            await update.message.reply_text(f"❌ Error processing audio file: {str(e)}")
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors."""
        logger.error(f"Update {update} caused error {context.error}")
    
    def setup_handlers(self):
        """Set up command and message handlers."""
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("play", self.play_command))
        self.application.add_handler(CommandHandler("stop", self.stop_command))
        self.application.add_handler(CommandHandler("pause", self.pause_command))
        self.application.add_handler(CommandHandler("resume", self.resume_command))
        self.application.add_handler(CommandHandler("list", self.list_command))
        self.application.add_handler(CommandHandler("current", self.current_command))
        self.application.add_handler(CommandHandler("storage", self.storage_command))
        self.application.add_handler(CommandHandler("volume", self.volume_command))
        
        # File handlers
        self.application.add_handler(MessageHandler(filters.AUDIO, self.handle_audio_file))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_audio_file))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_audio_file))
        
        # Error handler
        self.application.add_error_handler(self.error_handler)
    
    def run(self):
        """Run the bot."""
        print("🤖 Starting Music Play Bot...")
        print(f"📁 Download path: {config.download_path}")
        print(f"🎚️ Default volume: {int(config.default_volume * 100)}%")
        
        # Configure proxy if available
        
        
        
        builder = (
            Application.builder()
            .token(config.telegram_bot_token)
        )
        if config.has_proxy():
            print(f"🌐 Using SOCKS5 proxy: {config.socks5_proxy_url}")
            builder.proxy_url(config.socks5_proxy_url)
        else:
            print("🌐 No proxy configured - using direct connection")
        self.application = builder.build()
        
        # Set up handlers
        self.setup_handlers()
        
        print("🎵 Music Play Bot is running!")
        print("Press Ctrl+C to stop")
        
        # Run the bot using the synchronous run_polling method
        try:
            self.application.run_polling(drop_pending_updates=True)
        except KeyboardInterrupt:
            print("\n🛑 Stopping bot...")
        except Exception as e:
            print(f"❌ Bot error: {e}")
        finally:
            print("🔄 Bot stopped")

# Create bot instance
bot = MusicPlayBot()

if __name__ == "__main__":
    bot.run()