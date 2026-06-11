# 🤖 Azizjon AI Support Bot - Enhanced Version

Azizjon Asadov bilan AI, promptlar, kodlar va boshqa xizmatlar haqida ma'lumot olish uchun Telegram bot.

## ✨ Xususiyatlar

### 👤 Foydalanuvchi Uchun
- 📱 **Interaktiv Menu Sistema** - 7 ta asosiy menyu
- 🏠 Home - Bosh sahifa
- 📚 Services - Xizmatlar to'liq ma'lumoti
- 👤 About - Azizjon Asadov haqida
- 📖 Tutorials - Darsliklar (hozircha bo'sh)
- 💻 Prompts & Codes - AI promptlari va kodlari
- 🎮 Games - O'yinlar (hozircha bo'sh)
- 📞 Contact - Azizjon bilan bog'lanish

### 🔐 Admin Uchun
- `/admin` - Admin buyruqlari
- `/stats` - Statistika
- `/users` - Foydalanuvchilar ro'yxati
- `/broadcast` - Hamma userga xabar
- `/ban` - Userni block
- `/unban` - Userni unlock
- `/keywords_list` - Kalit suzlar
- `/add_keyword` - Yangi kalit suz qo'shish
- **Reply System** - Adminning xabariga reply qilsang user'ga javob ketadi

### 💬 Auto-Response
- Kalit suzlarga avtomatik javoblar
- Rasm, video, document support

## 🚀 O'rnatish

### 1. Fayllarni yuklab oling
```bash
git clone https://github.com/azizasadov935-hue/telegram-support-bot.git
cd telegram-support-bot
```

### 2. Dependencies o'rnating
```bash
pip install -r requirements.txt
```

### 3. .env faylini sozlang
```bash
cp .env.example .env
```

**Edit `.env`:**
```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_admin_id
```

### 4. Botni ishga tushiring
```bash
python main.py
```

## 🔑 Environment Variables

| Variable | Tavsif |
|----------|---------|
| `BOT_TOKEN` | Telegram Bot Token (@BotFather dan olingan) |
| `ADMIN_ID` | Admin'ning Telegram ID'si (@userinfobot dan olingan) |

## 📱 Bot Menyu

```
🏠 Home - Bosh sahifa
├── 📚 Services - Xizmatlar
│   ├── 🤖 Telegram Botlar
│   ├── 🧠 AI Yechimlari
│   ├── 🔄 Biznes Avtomatlashtirish
│   ├── 🔌 API Integratsiyalari
│   ├── 💻 Web Development
│   ├── 🎬 AI Media
│   └── ⚙️ Maxsus Dasturiy Yechimlar
├── 👤 About Azizjon - Azizjon haqida
├── 📖 Tutorials - Darsliklar
├── 💻 Prompts & Codes
│   ├── 📝 Video Promptlar
│   ├── 🎨 Rasm Promptlar
│   ├── 🌐 Web Sayt Promptlar
│   └── 💻 Umumiy Codlar
├── 🎮 Games - O'yinlar
└── 📞 Contact - Bog'lanish
```

## 🔐 Admin Buyruqlari

### Statistika
```
/stats
→ Jami users, faol users, bloklangan users
```

### Foydalanuvchilar
```
/users
→ Barcha users ro'yxati ID, username, ism bilan
```

### Broadcast
```
/broadcast Salom hammaga!
→ Hamma active users'ga xabar yuborish
```

### Ban/Unban
```
/ban 123456789
/unban 123456789
→ Userni block qilish yoki unlock qilish
```

### Kalit Suzlar
```
/keywords_list
→ Mavjud kalit suzlar va javoblarni ko'rish

/add_keyword
→ Format: keyword | response
   Misol: Salom | Assalamu alaikum! 👋
```

## 💬 Admin Reply System

1. Foydalanuvchi bot'ga xabar yuborganda, siz unga javob olasiz
2. Javobli xabarning tagiga reply qiling
3. Javob avtomatik foydalanuvchiga ketadi
4. Rasm, video, document ham jo'natish mumkin

## 🌐 Railway'ga Deploy Qilish

### 1. Railway Account yarating
https://railway.app

### 2. GitHub Repository'ni ulang

### 3. Environment Variables o'rnating
```
BOT_TOKEN = your_token
ADMIN_ID = your_admin_id
```

### 4. Procfile yarating (agar kerak bo'lsa)
```
worker: python main.py
```

## 📊 Data Storage

- Users set'da saqlangan (RAM'da)
- Banned users set'da saqlangan
- User info va keywords dictionary'da saqlangan
- Persistent storage uchun database qo'shish mumkin

## 🛠️ Texnologiyalar

- **Python 3.11**
- **aiogram 3.4.1** - Telegram Bot Framework
- **python-dotenv** - Environment variables

## 📝 Fayl Strukturi

```
telegram-support-bot/
├── main.py              # Bot kodi
├── requirements.txt     # Dependencies
├── runtime.txt         # Python version (Railway)
├── .env.example        # Environment template
├── .env                # Local configuration (gitignore'da)
└── README.md           # Bu fayl
```

## 🐛 Muammolari Tuzatish

### Error: "Bot token not valid"
- BOT_TOKEN'ni to'g'ri ekanini tekshiring
- @BotFather'dan yangi token oling

### Error: "ADMIN_ID topilmadi"
- ADMIN_ID to'g'ri ekanini tekshiring
- @userinfobot'dan ID ni oling

### Bot javob bermayapti
- Internet ulanganligini tekshiring
- Bot @BotFather'da faol ekanini tekshiring
- `python main.py` qayta ishga tushiring

## 📞 Support

**Azizjon Asadov:**
- 🌐 Portfolio: https://azizasadov.is-a.dev
- 💬 Telegram: https://t.me/Azizjon_Asadov
- 🐙 GitHub: https://github.com/azizasadov935-hue

## 📄 Litsenziya

MIT

---

**Versiya:** 2.0 (Enhanced)
**Oxirgi yangilash:** 2024
