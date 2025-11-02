#!/usr/bin/env python3
"""
Test script for Music Play Bot
Verifies that all dependencies are installed and configured correctly.
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import pygame
        print("✅ pygame imported successfully")
    except ImportError as e:
        print(f"❌ pygame import failed: {e}")
        return False
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError as e:
        print(f"❌ python-telegram-bot import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        from mutagen import File
        print("✅ mutagen imported successfully")
    except ImportError as e:
        print(f"❌ mutagen import failed: {e}")
        return False
    
    return True

def test_audio():
    """Test audio system."""
    print("\n🔊 Testing audio system...")
    
    try:
        import pygame
        pygame.mixer.pre_init()
        pygame.mixer.init()
        print("✅ Audio system initialized successfully")
        pygame.mixer.quit()
        return True
    except Exception as e:
        print(f"❌ Audio system test failed: {e}")
        return False

def test_config():
    """Test configuration loading."""
    print("\n⚙️ Testing configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found. Please create it from .env.example")
        return False
    
    try:
        sys.path.insert(0, 'src')
        from src.config import config
        
        if config.telegram_bot_token == 'your_bot_token_here':
            print("⚠️ Telegram bot token not configured in .env file")
            return False
        
        print("✅ Configuration loaded successfully")
        print(f"   📁 Download path: {config.download_path}")
        print(f"   📏 Max file size: {config.max_file_size_mb}MB")
        
        if config.has_proxy():
            print(f"   🌐 SOCKS5 Proxy: {config.socks5_proxy_url}")
        else:
            print("   🌐 No proxy configured (direct connection)")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_directories():
    """Test directory structure."""
    print("\n📁 Testing directories...")
    
    required_dirs = ['src', 'downloads']
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}/ exists")
        else:
            print(f"❌ {directory}/ missing")
            return False
    
    return True

def main():
    """Run all tests."""
    print("🎵 Music Play Bot - System Test\n")
    
    tests = [
        test_directories,
        test_imports,
        test_audio,
        test_config
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot should work correctly.")
        print("\n🚀 To start the bot, run: python main.py")
    else:
        print("❌ Some tests failed. Please fix the issues before running the bot.")
        if passed < total - 1:
            print("💡 Try running: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()