#!/bin/bash

# Telegram Support Bot - Local Setup Script

echo "🤖 Telegram Support Bot o'rnatilmoqda..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 o'rnatilmagan. Python 3.11+ o'rnating."
    exit 1
fi

echo "✅ Python topildi"

# Create virtual environment
echo "📦 Virtual environment yaratilmoqda..."
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment faol"

# Install dependencies
echo "📚 Dependencies o'rnatilmoqda..."
pip install -r requirements.txt

echo "✅ Dependencies o'rnatildi"

# Check .env file
if [ ! -f .env ]; then
    echo "📝 .env fayli yaratilmoqda..."
    cp .env.example .env
    echo "⚠️ .env faylini to'ldiring:"
    echo "   - BOT_TOKEN"
    echo "   - ADMIN_ID"
fi

echo ""
echo "🎉 O'rnatish tugallandi!"
echo ""
echo "Botni ishga tushirish uchun:"
echo "  python main.py"
echo ""
