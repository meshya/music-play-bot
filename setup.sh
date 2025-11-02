#!/bin/bash

# Music Play Bot Setup Script
echo "🎵 Setting up Music Play Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $python_version is installed, but Python $required_version or higher is required."
    exit 1
fi

echo "✅ Python $python_version detected"

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "📦 Installing pip..."
    sudo apt update
    sudo apt install -y python3-pip
fi

# Install system dependencies for audio
echo "🔊 Installing system audio dependencies..."
sudo apt update
sudo apt install -y python3-dev portaudio19-dev libasound2-dev

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your Telegram bot token"
fi

# Create downloads directory
mkdir -p downloads

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get a bot token from @BotFather on Telegram"
echo "2. Edit .env file and add your bot token"
echo "3. Run: source venv/bin/activate"
echo "4. Run: python main.py"
echo ""
echo "🎵 Enjoy your Music Play Bot!"