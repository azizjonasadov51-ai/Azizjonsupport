# 🚀 Tezkor Boshlash Qo'llanmasi

## 1️⃣ O'rnatish (5 daqiqa)

### Windows
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Mac/Linux
```bash
pip3 install -r requirements.txt
```

## 2️⃣ Konfiguratsiya

```bash
cp .env.example .env
```

**Edit `.env`:**
```env
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
ADMIN_ID=YOUR_ADMIN_ID_HERE
```

**Bot Token olish (@BotFather):**
1. Telegramda @BotFather'ga xabar yuboring
2. `/newbot` yuboring
3. Bot uchun nom va username tanlang
4. Token oling va `.env` fayliga qo'ying

**Admin ID olish (@userinfobot):**
1. Telegramda @userinfobot'ga xabar yuboring
2. ID'ni ko'ring va `.env` faylida ADMIN_ID o'rnating

## 3️⃣ Botni Ishga Tushirish

```bash
python main.py
```

**Muvaffaqiyat! Bot Telegramda faol bo'ladi** 🎉

## 📱 Bot Menyu

```
🏠 Home - Bosh sahifa
📚 Services - Xizmatlar
👤 About Azizjon - Azizjon haqida
📖 Tutorials - Darsliklar
💻 Prompts & Codes - Promptlar va Kodlar
🎮 Games - O'yinlar
📞 Contact - Azizjon bilan bog'lanish
```

## 🔐 Admin Buyruqlari

```
/admin - Admin buyruqlari
/stats - Statistika
/users - Foydalanuvchilar ro'yxati
/broadcast Salom - Hamma userga xabar
/ban 123456789 - Userni block
/unban 123456789 - Userni unlock
/keywords_list - Kalit suzlar
/add_keyword - Yangi kalit suz qo'shish
```

## ⚡ Reply System

Admin'ning xabariga Reply qilsang → Javob avtomatik user'ga ketadi!

## 🌐 Railway'ga Deploy Qilish

1. GitHub'da repository yarating
2. Railway.app'da account yarating
3. GitHub repo'ni ulang
4. Environment variables o'rnating:
   - `BOT_TOKEN`
   - `ADMIN_ID`

Bot 24/7 faol bo'ladi! 🚀

## 📞 Muammolar

**Bot javob bermayapti?**
```
1. BOT_TOKEN'ni tekshiring
2. Internet ulanganligini tekshiring
3. Bot @BotFather'da faol ekanini tekshiring
```

**Admin ID xatoligi?**
```
@userinfobot'dan ID oling va .env'ga qo'ying
```

---

**Savollar?** https://t.me/Azizjon_Asadov
