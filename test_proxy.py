#!/usr/bin/env python3
"""
SOCKS5 Proxy Test Utility for Music Play Bot
Tests if the configured SOCKS5 proxy is working correctly.
"""

import sys
import asyncio
import os

# Add the src directory to the path
sys.path.insert(0, 'src')

async def test_proxy():
    """Test SOCKS5 proxy connection."""
    try:
        from src.config import config
        
        if not config.has_proxy():
            print("❌ No SOCKS5 proxy configured in .env file")
            print("💡 Add SOCKS5_PROXY_URL=socks5://host:port to your .env file")
            return False
        
        print(f"🌐 Testing SOCKS5 proxy: {config.socks5_proxy_url}")
        
        # Test with httpx and SOCKS5
        import httpx
        
        # Create client with SOCKS5 proxy
        proxy_config = config.get_proxy_config()
        
        async with httpx.AsyncClient(**proxy_config, timeout=30.0) as client:
            print("🔍 Testing connection to Telegram API...")
            
            # Test connection to Telegram API
            response = await client.get("https://api.telegram.org")
            
            if response.status_code == 200:
                print("✅ Proxy connection successful!")
                print(f"   Status: {response.status_code}")
                print(f"   Response size: {len(response.content)} bytes")
                return True
            else:
                print(f"❌ Telegram API returned status: {response.status_code}")
                return False
                
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install httpx[socks]")
        return False
    except Exception as e:
        print(f"❌ Proxy test failed: {e}")
        print("💡 Check if:")
        print("   - Proxy server is running")
        print("   - Proxy URL format is correct: socks5://host:port")
        print("   - Authentication credentials are correct (if needed)")
        return False

async def test_telegram_bot():
    """Test Telegram bot with proxy."""
    try:
        from src.config import config
        from telegram.request import HTTPXRequest
        from telegram import Bot
        
        if not config.telegram_bot_token or config.telegram_bot_token == 'your_bot_token_here':
            print("⚠️ Telegram bot token not configured - skipping bot test")
            return True
        
        print("🤖 Testing Telegram bot with proxy...")
        
        if config.has_proxy():
            # Create bot with proxy
            request = HTTPXRequest(
                proxy_url=config.socks5_proxy_url,
                read_timeout=20,
                write_timeout=20,
                connect_timeout=20
            )
            bot = Bot(token=config.telegram_bot_token, request=request)
        else:
            bot = Bot(token=config.telegram_bot_token)
        
        # Test bot connection
        me = await bot.get_me()
        print(f"✅ Bot connection successful!")
        print(f"   Bot name: @{me.username}")
        print(f"   Bot ID: {me.id}")
        
        await bot.close()
        return True
        
    except Exception as e:
        print(f"❌ Telegram bot test failed: {e}")
        return False

def main():
    """Run proxy tests."""
    print("🌐 SOCKS5 Proxy Test Utility\n")
    
    async def run_tests():
        results = []
        
        # Test basic proxy connection
        print("1. Testing SOCKS5 Proxy Connection")
        print("=" * 40)
        results.append(await test_proxy())
        print()
        
        # Test Telegram bot with proxy
        print("2. Testing Telegram Bot with Proxy")
        print("=" * 40)
        results.append(await test_telegram_bot())
        print()
        
        # Summary
        passed = sum(results)
        total = len(results)
        
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All proxy tests passed!")
            print("✅ Your SOCKS5 proxy is working correctly with the bot")
        else:
            print("❌ Some proxy tests failed")
            print("💡 Check your proxy configuration and network connection")
    
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\n👋 Test cancelled by user")

if __name__ == "__main__":
    main()