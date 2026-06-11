import asyncio
import logging
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# Load .env file
load_dotenv()

# Configuration
TOKEN = os.getenv("TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_CHAT_ID", "7534509370"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data storage
users = set()
banned_users = set()
users_data = {}  # Store user info
keywords_responses = {}  # Store keyword->response mapping
user_projects = {}  # Store user project details

# SERVICES DATA
SERVICES = {
    "ai_sales": {
        "name": "🤖 AI Sotuv Menejeri",
        "problem": "Mijozlar tunda ham yozadi, jamoa offline.",
        "solution": "AI menejer 3 soniyada javob beradi va tayyor mijozni yo'naltiradi.",
        "features": ["24/7 javob", "Lead filtrlash", "CRM integratsiya", "Ko'p tilli"],
        "price": "2,850,000+ so'm"
    },
    "telegram_bot": {
        "name": "📱 Telegram Bot",
        "problem": "Telegramda tartibsizlik.",
        "solution": "Bot hammasini avtomatlashtiradi.",
        "features": ["Avto buyurtma", "To'lov", "Admin panel", "Broadcast"],
        "price": "1,790,000+ so'm"
    },
    "premium_website": {
        "name": "🌐 Premium Web Sayt",
        "problem": "Sayt ajralmaydi.",
        "solution": "Glassmorphism, animatsiya, 3D UX.",
        "features": ["3D effektlar", "Animatsiya", "Unique dizayn", "Lighthouse 95+"],
        "price": "4,650,000+ so'm"
    },
    "ai_agents": {
        "name": "🦾 AI Agentlar",
        "problem": "Vaqt oddiy vazifalarga ketadi.",
        "solution": "AI agentlar rutinani avtomatlashtiradi.",
        "features": ["Mustaqil ishlash", "Ko'p vazifa", "API ulash", "O'rganish"],
        "price": "3,200,000+ so'm"
    },
    "ai_chatbot": {
        "name": "💬 AI Chatbotlar",
        "problem": "Bir xil savollar takrorlanadi.",
        "solution": "80% savollarga avtomatik javob.",
        "features": ["Tez javob", "Ko'p kanal", "Analitika", "O'qitish"],
        "price": "1,950,000+ so'm"
    },
    "landing_page": {
        "name": "📄 Landing Page",
        "problem": "Trafik bor, konversiya yo'q.",
        "solution": "Landing konversiyani 2-3x oshiradi.",
        "features": ["Premium dizayn", "Mobile first", "SEO", "Tez yuklanish"],
        "price": "2,450,000+ so'm"
    },
    "corporate_site": {
        "name": "🏢 Korporativ Web Sayt",
        "problem": "Eski sayt ishonchni yo'qotadi.",
        "solution": "Zamonaviy vitrina + admin panel.",
        "features": ["Premium UI", "Admin panel", "Ko'p til", "CMS"],
        "price": "4,650,000+ so'm"
    },
    "web_platform": {
        "name": "🖥️ Web Platformalar",
        "problem": "Excel yetmayapti.",
        "solution": "To'liq web platforma.",
        "features": ["SaaS", "To'lov", "Dashboard", "API"],
        "price": "6,500,000+ so'm"
    },
    "crm_integration": {
        "name": "🔗 CRM Integratsiyalar",
        "problem": "Leadlar CRM ga tushmaydi.",
        "solution": "Avtomatik CRM integratsiya.",
        "features": ["Avto lead", "Sinxron", "Hisobot", "Voronka"],
        "price": "2,800,000+ so'm"
    },
    "automation": {
        "name": "⚙️ Biznes Avtomatlashtirish",
        "problem": "15 qadam, 3 xodim, 2 soat.",
        "solution": "Workflow: murojaat → yetkazish.",
        "features": ["Workflow", "Vaqt tejash", "Xatosizlik", "Masshtab"],
        "price": "4,200,000+ so'm"
    },
    "workflow": {
        "name": "🔄 Workflow Automation",
        "problem": "Tizimlar alohida.",
        "solution": "Trigger-based avtomat oqim.",
        "features": ["Trigger", "Multi-app", "Monitoring", "Alert"],
        "price": "3,500,000+ so'm"
    },
    "api_integration": {
        "name": "🔌 API Integratsiyalar",
        "problem": "Qo'lda ma'lumot ko'chirish.",
        "solution": "Real-time sinxronizatsiya.",
        "features": ["Real-time", "Webhook", "Xavfsizlik", "Docs"],
        "price": "2,400,000+ so'm"
    },
    "ai_video": {
        "name": "🎬 AI Video Generation",
        "problem": "Video qimmat va sekin.",
        "solution": "1 kunda tayyor video.",
        "features": ["Tez", "Arzon", "Ko'p format", "AI avatar"],
        "price": "650,000+ so'm"
    },
    "ai_image": {
        "name": "🎨 AI Image Generation",
        "problem": "Dizayner sekin.",
        "solution": "2 soatda 10 variant.",
        "features": ["Tez iteratsiya", "Ko'p variant", "Sifat", "Brend"],
        "price": "350,000+ so'm"
    },
    "design_posters": {
        "name": "📐 Dizayn va Posterlar",
        "problem": "Standart dizayn ko'rinmaydi.",
        "solution": "Premium trend dizayn.",
        "features": ["Premium", "Print ready", "Brend", "Tez"],
        "price": "350,000+ so'm"
    },
    "smm_design": {
        "name": "📱 SMM Dizaynlar",
        "problem": "Brend tanilmaydi.",
        "solution": "Kontent kalendari + shablonlar.",
        "features": ["Shablonlar", "Kalendari", "Brend kit", "Tez post"],
        "price": "450,000+ so'm"
    },
    "3d_visual": {
        "name": "🎯 3D Reklama Vizuallari",
        "problem": "Oddiy foto yetarli emas.",
        "solution": "Wow effektli 3D vizual.",
        "features": ["3D model", "Animatsiya", "Wow", "Premium"],
        "price": "1,200,000+ so'm"
    },
    "startup_mvp": {
        "name": "🚀 Startup MVP Development",
        "problem": "Qayerdan boshlash noma'lum.",
        "solution": "Tez launch + investor ready.",
        "features": ["Tez launch", "Investor ready", "Iteratsiya", "Full stack"],
        "price": "8,500,000+ so'm"
    },
    "prompt_engineering": {
        "name": "✨ Prompt Engineering",
        "problem": "AI natijasi barqaror emas.",
        "solution": "Optimizatsiya va shablonlar.",
        "features": ["Barqaror", "Shablonlar", "Optimizatsiya", "Training"],
        "price": "890,000+ so'm"
    }
}

# FSM States
class MenuStates(StatesGroup):
    main_menu = State()
    services = State()
    service_selected = State()
    project_name = State()
    project_description = State()
    budget = State()
    contact_info = State()
    prompts_codes = State()
    contact = State()
    awaiting_message = State()

# ==================== KEYBOARD LAYOUTS ====================

def get_main_keyboard():
    """Main menu keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏠 Home"), KeyboardButton(text="📚 Services")],
            [KeyboardButton(text="👤 About Azizjon"), KeyboardButton(text="📖 Tutorials")],
            [KeyboardButton(text="💻 Prompts & Codes"), KeyboardButton(text="🎮 Games")],
            [KeyboardButton(text="📞 Contact")]
        ],
        resize_keyboard=True
    )

def get_services_keyboard():
    """Services menu keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛍️ Barcha Xizmatlar"), KeyboardButton(text="📋 Kategoriyalar")],
            [KeyboardButton(text="❓ Qanday Tanlov?"), KeyboardButton(text="◀️ Orqaga")]
        ],
        resize_keyboard=True
    )

def get_services_inline_keyboard():
    """Inline keyboard for all services"""
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    
    buttons = []
    for service_key, service in SERVICES.items():
        buttons.append([InlineKeyboardButton(
            text=service['name'],
            callback_data=f"service_{service_key}"
        )])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_prompts_codes_keyboard():
    """Prompts & Codes menu keyboard"""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Video Promptlar"), KeyboardButton(text="🎨 Rasm Promptlar")],
            [KeyboardButton(text="🌐 Web Sayt Promptlar"), KeyboardButton(text="💻 Umumiy Codlar")],
            [KeyboardButton(text="◀️ Orqaga")]
        ],
        resize_keyboard=True
    )

# ==================== MESSAGES ====================

START_MESSAGE = """
Assalamu alaikum! 👋

Siz <b>Azizjon Asadov</b> ning AI Bot'iga xush kelibsiz!

🤖 Men sizga quyidagilar bilan yordamchi bo'la olaman:
✅ AI yechimlari haqida to'liq ma'lumot
✅ Telegram botlar yaratish va dizayn
✅ AI Promptlar va Kodlar
✅ Biznes avtomatlashtirish tizimlar
✅ Zamonaviy veb-saytlar yaratish
✅ Raqamli texnologik yechimlar
✅ Va boshqa ko'p narsalar...

📌 Quyidagi bo'limlardan birini tanlang:

📚 <b>Services</b> - Xizmatlar haqida to'liq ma'lumot
👤 <b>About</b> - Azizjon Asadov haqida
📖 <b>Tutorials</b> - Darsliklar
💻 <b>Prompts & Codes</b> - AI Promptlar va Kodlar
📞 <b>Contact</b> - To'g'ridan-to'g'ri bog'lanish

Bosh sahifadan boshlaylik! 👇
"""

SERVICES_MESSAGE = """
📚 <b>Xizmatlar</b>

Azizjon Asadov quyidagi xizmatlarni taqdim etadi:

🤖 <b>AI Yechimlari</b>
💬 Chatbotlar, AI Agentlar, Sotuv Menejerilari

📱 <b>Telegram va Web</b>
🤖 Botlar, Veb-saytlar, Landing Page'lar

🔄 <b>Avtomatlashtirish</b>
⚙️ CRM, Workflow, API Integratsiyalar

🎨 <b>Dizayn va Media</b>
🎬 Video, Rasm, 3D, Posterlar, SMM

🚀 <b>Loyihalar</b>
🚀 MVP, Startup, SaaS Platformalar

📌 Quyidagi xizmatlardan birini tanlang yoki to'liq ro'yxatni ko'rish uchun "Barcha Xizmatlar" tugmasini bosing.
"""

ABOUT_MESSAGE = """
👤 <b>Azizjon Asadov Haqida</b>

<b>Azizjon Asadov</b> — sun'iy intellekt, avtomatlashtirish tizimlari va raqamli texnologiyalar sohasida faoliyat yurituvchi mutaxassis.

<b>Hozirgi Pozitsiya:</b>
Izdihom PR/Marketing Agentligida
• Sun'iy Intellekt Mutaxassisi (AI Specialist)
• Team Leader
• AI Departament Rahbari

<b>Asosiy Faoliyat:</b>
✅ AI texnologiyalarini real biznes jarayonlariga joriy etish
✅ Zamonaviy veb-platformalar yaratish
✅ Telegram botlar ishlab chiqish
✅ Raqamli mahsulotlar yaratish

<b>Asosiy Yo'nalishlari:</b>
🤖 Sun'iy intellekt (AI) yechimlari
🔤 Telegram botlar ishlab chiqish
🔌 API integratsiyalari va avtomatlashtirish
💻 Web Development
📊 AI Agentlar va AI Workflow tizimlari
🎨 Kontent yaratish va AI Media Production
📈 Raqamli marketing uchun AI texnologiyalari
⚙️ Biznes jarayonlarini optimallashtirish

<b>Rasmiy Portfolio:</b>
🌐 https://azizasadov.is-a.dev

<b>Hamkorlik Takliflari Qabul Qilinadi:</b>
✨ AI yechimlar
✨ Telegram botlar
✨ Veb-saytlar
✨ Avtomatlashtirish tizimlari
✨ Media loyihalar
"""

TUTORIALS_MESSAGE = """
📖 <b>Darsliklar</b>

Hozircha darsliklar mavjud emas.

Agar sizga darsliklar kerak bo'lsa, aloqa qiling:
📞 /contact
"""

PROMPTS_CODES_MESSAGE = """
💻 <b>Promptlar va Kodlar</b>

Hozircha promptlar va kodlar mavjud emas.

Olarni qo'shish uchun keyinroq qayta urinib ko'ring.
"""

GAMES_MESSAGE = """
🎮 <b>O'yinlar</b>

Hozircha o'yinlar mavjud emas.
"""

CONTACT_MESSAGE = """
📞 <b>Azizjon Asadov bilan Bog'lanish</b>

Azizjon bilan to'g'ridan-to'g'ri bog'lanish uchun:

👤 <b>Telegram Profile:</b> https://t.me/Azizjon_Asadov

Quyida xabari yuborishingiz mumkin, u sizga javob qaytaradi:
"""

# ==================== COMMAND HANDLERS ====================

@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    """Handle /start command"""
    if message.from_user.id in banned_users:
        return
    
    user_id = message.from_user.id
    users.add(user_id)
    
    # Store user data
    users_data[user_id] = {
        'username': message.from_user.username,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'joined_at': datetime.now().isoformat(),
        'last_message': datetime.now().isoformat()
    }
    
    await message.answer(START_MESSAGE, parse_mode='HTML', reply_markup=get_main_keyboard())
    await state.set_state(MenuStates.main_menu)


@dp.message(Command("admin"))
async def admin_handler(message: Message):
    """Show admin commands"""
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
    
    admin_text = """
🔐 <b>Admin Panel Buyruqlari</b>

/stats - Statistika ko'rish
/users - Foydalanuvchilar ro'yxati
/broadcast Salom hammaga - Hamma userga xabar yuborish
/ban 123456789 - Userni block qilish
/unban 123456789 - Userni unlock qilish
/keywords_list - Kalit suzlar ro'yxati
/add_keyword - Yangi kalit suz qo'shish
"""
    await message.answer(admin_text, parse_mode='HTML')


@dp.message(Command("stats"))
async def stats_handler(message: Message):
    """Show statistics"""
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
    
    stats_text = f"""
📊 <b>Statistika</b>

👥 Jami foydalanuvchilar: {len(users)}
✅ Faol foydalanuvchilar: {len(users) - len(banned_users)}
❌ Bloklangan foydalanuvchilar: {len(banned_users)}
"""
    await message.answer(stats_text, parse_mode='HTML')


@dp.message(Command("users"))
async def users_handler(message: Message):
    """Show all users"""
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
    
    if not users:
        return await message.answer("📭 Foydalanuvchilar mavjud emas.")
    
    text = "👥 <b>Foydalanuvchilar</b>\n\n"
    for i, user_id in enumerate(users, 1):
        status = "🚫" if user_id in banned_users else "✅"
        user_info = users_data.get(user_id, {})
        username = user_info.get('username', 'N/A')
        first_name = user_info.get('first_name', 'N/A')
        text += f"{i}. {status} <code>{user_id}</code> - @{username} ({first_name})\n"
    
    # Split if too long
    if len(text) > 4096:
        chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
        for chunk in chunks:
            await message.answer(chunk, parse_mode='HTML')
    else:
        await message.answer(text, parse_mode='HTML')


@dp.message(Command("ban"))
async def ban_handler(message: Message):
    """Ban a user"""
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
    
    try:
        user_id = int(message.text.split()[1])
        banned_users.add(user_id)
        await message.answer(f"✅ Foydalanuvchi <code>{user_id}</code> bloklandi.", parse_mode='HTML')
    except:
        await message.answer("❌ Format: /ban USER_ID")


@dp.message(Command("unban"))
async def unban_handler(message: Message):
    """Unban a user"""
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
    
    try:
        user_id = int(message.text.split()[1])
        banned_users.discard(user_id)
        await message.answer(f"✅ Foydalanuvchi <code>{user_id}</code> unlock qilindi.", parse_mode='HTML')
    except:
        await message.answer("❌ Format: /unban USER_ID")


@dp.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    """Send message to all users"""
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
    
    try:
        text = message.text.replace("/broadcast ", "")
        if not text:
            return await message.answer("❌ Xabar matnini kiriting.\nMisol: /broadcast Salom hammaga!")
        
        success = 0
        for user_id in users:
            if user_id not in banned_users:
                try:
                    await bot.send_message(user_id, text, parse_mode='HTML')
                    success += 1
                except:
                    pass
        
        await message.answer(f"✅ Broadcast yuborildi: {success} ta userga")
    except Exception as e:
        await message.answer(f"❌ Xatolik: {str(e)}")


@dp.message(Command("keywords_list"))
async def keywords_list_handler(message: Message):
    """Show all keywords"""
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
    
    if not keywords_responses:
        return await message.answer("📭 Kalit suzlar mavjud emas.")
    
    text = "🔑 <b>Kalit Suzlar va Javoblar</b>\n\n"
    for i, (keyword, response) in enumerate(keywords_responses.items(), 1):
        text += f"{i}. <b>{keyword}</b>\n→ {response[:50]}...\n\n"
    
    if len(text) > 4096:
        chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
        for chunk in chunks:
            await message.answer(chunk, parse_mode='HTML')
    else:
        await message.answer(text, parse_mode='HTML')


@dp.message(Command("add_keyword"))
async def add_keyword_handler(message: Message):
    """Add new keyword"""
    if message.from_user.id != ADMIN_ID:
        return await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo'q.")
    
    await message.answer("🔑 Kalit suz va javobni quyidagi formatda yuboring:\n\nkalit_suz | javob\n\nMisol:\nSalom | Assalamu alaikum! 👋")


# ==================== MENU HANDLERS ====================

@dp.message(lambda m: m.text == "🏠 Home")
async def home_handler(message: Message, state: FSMContext):
    """Home menu"""
    if message.from_user.id in banned_users:
        return
    
    # ADMIN SEES DIFFERENT MENU
    if message.from_user.id == ADMIN_ID:
        admin_text = "🔐 <b>Admin Panel</b>\n\n"
        admin_text += "/stats - Statistika\n"
        admin_text += "/users - Foydalanuvchilar ro'yxati\n"
        admin_text += "/ban [ID] - Foydalanuvchini bloklash\n"
        admin_text += "/unban [ID] - Blokirovkani olib tashlash\n"
        admin_text += "/broadcast [xabar] - Hammasiga xabar jo'natish\n"
        admin_text += "/keywords_list - Kalit so'zlar ro'yxati\n"
        admin_text += "/add_keyword - Kalit so'z qo'shish"
        
        admin_keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="/stats"), KeyboardButton(text="/users")],
                [KeyboardButton(text="/keywords_list")]
            ],
            resize_keyboard=True
        )
        await message.answer(admin_text, parse_mode='HTML', reply_markup=admin_keyboard)
        return
    
    await message.answer(START_MESSAGE, parse_mode='HTML', reply_markup=get_main_keyboard())
    await state.set_state(MenuStates.main_menu)


@dp.message(lambda m: m.text == "📚 Services")
async def services_handler(message: Message, state: FSMContext):
    """Services menu"""
    if message.from_user.id in banned_users:
        return
    
    # ADMIN SHOULDN'T SEE SERVICES MENU
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔐 Admin uchun bu menu mavjud emas", parse_mode='HTML')
        return
    
    await message.answer(SERVICES_MESSAGE, parse_mode='HTML', reply_markup=get_services_keyboard())
    await state.set_state(MenuStates.services)


@dp.message(lambda m: m.text == "🛍️ Barcha Xizmatlar")
async def all_services_handler(message: Message, state: FSMContext):
    """Show all services with inline buttons"""
    if message.from_user.id in banned_users:
        return
    
    text = "🛍️ <b>BARCHA XIZMATLAR</b>\n\n"
    text += "Quyidagi xizmatlardan birini tanlang:\n\n"
    
    await message.answer(text, parse_mode='HTML', reply_markup=get_services_inline_keyboard())
    await state.set_state(MenuStates.service_selected)


@dp.callback_query(lambda c: c.data.startswith("service_"))
async def service_selected_handler(callback_query, state: FSMContext):
    """Handle service selection"""
    from aiogram import types
    
    service_key = callback_query.data.replace("service_", "")
    
    if service_key not in SERVICES:
        await callback_query.answer("Xizmat topilmadi", show_alert=True)
        return
    
    service = SERVICES[service_key]
    
    # Store selected service
    user_id = callback_query.from_user.id
    if user_id not in user_projects:
        user_projects[user_id] = {}
    
    user_projects[user_id]['service_key'] = service_key
    user_projects[user_id]['service_name'] = service['name']
    
    # Show service details
    text = f"<b>{service['name']}</b>\n\n"
    text += f"<b>Problem:</b> {service['problem']}\n\n"
    text += f"<b>Yechim:</b> {service['solution']}\n\n"
    text += f"<b>Imkoniyatlar:</b>\n"
    for feature in service['features']:
        text += f"• {feature}\n"
    text += f"\n<b>Narxi:</b> {service['price']}\n\n"
    text += "👇 <i>Loyihani muhokama qilish uchun \"Loyihani Muhokama Qil\" tugmasini bosing</i>"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💬 Loyihani Muhokama Qil", callback_data=f"discuss_{service_key}")],
        [InlineKeyboardButton(text="◀️ Orqaga", callback_data="back_to_services")]
    ])
    
    await callback_query.message.edit_text(text, parse_mode='HTML', reply_markup=keyboard)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data.startswith("discuss_"))
async def discuss_project_handler(callback_query, state: FSMContext):
    """Start project discussion form"""
    service_key = callback_query.data.replace("discuss_", "")
    
    user_id = callback_query.from_user.id
    if user_id not in user_projects:
        user_projects[user_id] = {}
    
    user_projects[user_id]['service_key'] = service_key
    user_projects[user_id]['service_name'] = SERVICES[service_key]['name']
    
    # Ask for project name
    text = f"📝 <b>{SERVICES[service_key]['name']}</b> uchun loyiha\n\n"
    text += "Loyihangizning nomini yozing:\n"
    text += "<i>Masalan: E-commerce platformasi, AI Chatbot sistemasi, va hokazo...</i>"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_form")]
    ])
    
    await callback_query.message.edit_text(text, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(MenuStates.project_name)
    await callback_query.answer()


@dp.message(MenuStates.project_name)
async def project_name_handler(message: Message, state: FSMContext):
    """Get project name"""
    if message.from_user.id in banned_users:
        return
    
    user_id = message.from_user.id
    if user_id not in user_projects:
        user_projects[user_id] = {}
    
    user_projects[user_id]['project_name'] = message.text
    
    # Ask for description
    text = f"📝 <b>Loyiha tavsifi</b>\n\n"
    text += f"<b>Loyiha nomi:</b> {message.text}\n\n"
    text += "Endi loyihangiz haqida batafsil malumot yozing:\n"
    text += "<i>Masalan: Qo'shimcha talab va shartlar, dizayn tavsifi, xususiyatlar...</i>"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭️ Keyingi", callback_data="next_to_budget")]
    ])
    
    await message.answer(text, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(MenuStates.project_description)


@dp.message(MenuStates.project_description)
async def project_description_handler(message: Message, state: FSMContext):
    """Get project description"""
    if message.from_user.id in banned_users:
        return
    
    user_id = message.from_user.id
    if user_id not in user_projects:
        user_projects[user_id] = {}
    
    user_projects[user_id]['project_description'] = message.text
    
    # Ask for budget
    text = f"💰 <b>Byudjet</b>\n\n"
    text += f"<b>Loyiha nomi:</b> {user_projects[user_id].get('project_name', 'N/A')}\n"
    text += f"<b>Tavsifi:</b> {message.text}\n\n"
    text += "Endi aniqlanishni kutayotgan byudjet o'lchamini yozing:\n"
    text += "<i>Masalan: 2,500,000 so'm, 3,000,000+ so'm, batafsil muhokama kerak...</i>"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏭️ Keyingi", callback_data="next_to_contact")]
    ])
    
    await message.answer(text, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(MenuStates.budget)


@dp.message(MenuStates.budget)
async def budget_handler(message: Message, state: FSMContext):
    """Get budget and ask for contact"""
    if message.from_user.id in banned_users:
        return
    
    user_id = message.from_user.id
    if user_id not in user_projects:
        user_projects[user_id] = {}
    
    user_projects[user_id]['budget'] = message.text
    
    # Ask for contact info
    text = f"📞 <b>Aloqa malumoti</b>\n\n"
    text += f"<b>Loyiha nomi:</b> {user_projects[user_id].get('project_name', 'N/A')}\n"
    text += f"<b>Byudjet:</b> {message.text}\n\n"
    text += "Oxirgi qadamda, aloqa raqamingizni ulashing:\n"
    text += "<i>Quyidagi tugmani bosing va Telegram orqali telefon raqamingizni jo'nating</i>"
    
    from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📱 Raqamni ulash", request_contact=True)]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(text, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(MenuStates.contact_info)


@dp.message(MenuStates.contact_info)
async def contact_info_handler(message: Message, state: FSMContext):
    """Get contact info and submit form to admin"""
    if message.from_user.id in banned_users:
        return
    
    user_id = message.from_user.id
    if user_id not in user_projects:
        user_projects[user_id] = {}
    
    # Get phone number from contact
    phone = None
    if message.contact:
        phone = message.contact.phone_number
    elif message.text:
        phone = message.text
    
    user_projects[user_id]['contact'] = phone
    
    # Get user info
    user_info = users_data.get(user_id, {})
    username = user_info.get('username', 'N/A')
    first_name = user_info.get('first_name', 'N/A')
    
    # Prepare message for admin
    admin_text = "<b>📋 YANGI LOYIHA MUROJAATI</b>\n\n"
    admin_text += f"<b>Xizmat:</b> {user_projects[user_id].get('service_name', 'N/A')}\n"
    admin_text += f"<b>Foydalanuvchi:</b> @{username} (ID: <code>{user_id}</code>)\n"
    admin_text += f"<b>Ism:</b> {first_name}\n"
    admin_text += f"<b>Loyiha nomi:</b> {user_projects[user_id].get('project_name', 'N/A')}\n"
    admin_text += f"<b>Tavsifi:</b> {user_projects[user_id].get('project_description', 'N/A')}\n"
    admin_text += f"<b>Byudjet:</b> {user_projects[user_id].get('budget', 'N/A')}\n"
    admin_text += f"<b>Telefon:</b> {phone}\n\n"
    admin_text += "💬 <i>Loyihani muhokama qilish uchun foydalanuvchiga javob yozing</i>"
    
    # Send to admin
    try:
        await bot.send_message(ADMIN_ID, admin_text, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Error sending to admin: {e}")
    
    # Confirm to user
    confirm_text = f"✅ <b>Raxmat!</b>\n\n"
    confirm_text += f"Sizning murojaatingiz jo'natildi.\n"
    confirm_text += f"Azizjon Asadov tez orada siz bilan bog'lanadi.\n\n"
    confirm_text += f"📊 <b>Sizning malumotlaringiz:</b>\n"
    confirm_text += f"• Xizmat: {user_projects[user_id].get('service_name', 'N/A')}\n"
    confirm_text += f"• Loyiha: {user_projects[user_id].get('project_name', 'N/A')}\n"
    confirm_text += f"• Byudjet: {user_projects[user_id].get('budget', 'N/A')}\n\n"
    confirm_text += "🔙 Bosh menyuga qaytish uchun /start ni yozing"
    
    await message.answer(confirm_text, parse_mode='HTML', reply_markup=get_main_keyboard())
    await state.set_state(MenuStates.main_menu)
    
    # Clear user project data
    del user_projects[user_id]


@dp.callback_query(lambda c: c.data == "back_to_services")
async def back_to_services_handler(callback_query, state: FSMContext):
    """Go back to services list"""
    await callback_query.message.edit_text(
        SERVICES_MESSAGE,
        parse_mode='HTML',
        reply_markup=get_services_keyboard()
    )
    await state.set_state(MenuStates.services)
    await callback_query.answer()


@dp.callback_query(lambda c: c.data == "cancel_form")
async def cancel_form_handler(callback_query, state: FSMContext):
    """Cancel form"""
    user_id = callback_query.from_user.id
    if user_id in user_projects:
        del user_projects[user_id]
    
    await callback_query.message.edit_text(
        SERVICES_MESSAGE,
        parse_mode='HTML',
        reply_markup=get_services_keyboard()
    )
    await state.set_state(MenuStates.services)
    await callback_query.answer()


@dp.message(lambda m: m.text == "👤 About Azizjon")
async def about_handler(message: Message, state: FSMContext):
    """About Azizjon"""
    if message.from_user.id in banned_users:
        return
    
    # ADMIN SHOULDN'T SEE THIS
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔐 Admin uchun bu menu mavjud emas", parse_mode='HTML')
        return
    
    await message.answer(ABOUT_MESSAGE, parse_mode='HTML', reply_markup=get_main_keyboard())
    await state.set_state(MenuStates.main_menu)


@dp.message(lambda m: m.text == "📖 Tutorials")
async def tutorials_handler(message: Message, state: FSMContext):
    """Tutorials menu"""
    if message.from_user.id in banned_users:
        return
    
    # ADMIN SHOULDN'T SEE THIS
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔐 Admin uchun bu menu mavjud emas", parse_mode='HTML')
        return
    
    await message.answer(TUTORIALS_MESSAGE, parse_mode='HTML', reply_markup=get_main_keyboard())


@dp.message(lambda m: m.text == "💻 Prompts & Codes")
async def prompts_codes_handler(message: Message, state: FSMContext):
    """Prompts & Codes menu"""
    if message.from_user.id in banned_users:
        return
    
    # ADMIN SHOULDN'T SEE THIS
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔐 Admin uchun bu menu mavjud emas", parse_mode='HTML')
        return
    
    await message.answer(PROMPTS_CODES_MESSAGE, parse_mode='HTML', reply_markup=get_prompts_codes_keyboard())
    await state.set_state(MenuStates.prompts_codes)


@dp.message(lambda m: m.text == "🎮 Games")
async def games_handler(message: Message, state: FSMContext):
    """Games menu"""
    if message.from_user.id in banned_users:
        return
    
    await message.answer(GAMES_MESSAGE, parse_mode='HTML', reply_markup=get_main_keyboard())


@dp.message(lambda m: m.text == "📞 Contact")
async def contact_handler(message: Message, state: FSMContext):
    """Contact menu"""
    if message.from_user.id in banned_users:
        return
    
    # ADMIN SHOULDN'T SEE THIS
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔐 Admin uchun bu menu mavjud emas", parse_mode='HTML')
        return
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📨 Xabar Yuborish", url="https://t.me/Azizjon_Asadov")]
        ]
    )
    await message.answer(CONTACT_MESSAGE, parse_mode='HTML', reply_markup=keyboard)
    await state.set_state(MenuStates.contact)


@dp.message(lambda m: m.text == "◀️ Orqaga")
async def back_handler(message: Message, state: FSMContext):
    """Back button"""
    if message.from_user.id in banned_users:
        return
    
    # ADMIN SHOULDN'T SEE THIS
    if message.from_user.id == ADMIN_ID:
        await message.answer("🔐 Admin uchun bu menu mavjud emas", parse_mode='HTML')
        return
    
    await message.answer("🏠 Bosh sahifaga qaytdingiz:", reply_markup=get_main_keyboard())
    await state.set_state(MenuStates.main_menu)


# ==================== MESSAGE HANDLER ====================

@dp.message()
async def message_handler(message: Message):
    """Handle all other messages"""
    if message.from_user.id in banned_users:
        return
    
    # ADMIN SHOULDN'T RECEIVE OWN MESSAGES
    if message.from_user.id == ADMIN_ID:
        return
    
    user_id = message.from_user.id
    users.add(user_id)
    
    # Update user data
    if user_id in users_data:
        users_data[user_id]['last_message'] = datetime.now().isoformat()
    
    # ADMIN REPLY SYSTEM
    if user_id == ADMIN_ID and message.reply_to_message:
        replied_text = message.reply_to_message.text or ""
        
        if "🆔 ID:" in replied_text:
            try:
                user_id_reply = int(replied_text.split("🆔 ID: ")[1].split("\n")[0])
                
                if message.text:
                    await bot.send_message(
                        user_id_reply,
                        f"📩 Admin javobi:\n\n{message.text}",
                        parse_mode='HTML'
                    )
                elif message.photo:
                    await bot.send_photo(
                        user_id_reply,
                        photo=message.photo[-1].file_id,
                        caption=message.caption or "📩 Admin javobi"
                    )
                elif message.video:
                    await bot.send_video(
                        user_id_reply,
                        video=message.video.file_id,
                        caption=message.caption or "📩 Admin javobi"
                    )
                elif message.document:
                    await bot.send_document(
                        user_id_reply,
                        document=message.document.file_id,
                        caption=message.caption or "📩 Admin javobi"
                    )
                
                await message.reply("✅ Xabar foydalanuvchiga yuborildi.")
            except Exception as e:
                await message.reply(f"❌ Xatolik: {str(e)}")
        
        return
    
    # CHECK KEYWORDS
    if message.text:
        for keyword, response in keywords_responses.items():
            if keyword.lower() in message.text.lower():
                await message.answer(response, parse_mode='HTML')
                return
    
    # SEND USER MESSAGE TO ADMIN
    user = message.from_user
    caption = f"""
📩 <b>Yangi xabar</b>

👤 Ism: {user.full_name}
🆔 ID: <code>{user.id}</code>
📛 Username: @{user.username if user.username else 'N/A'}
"""
    
    if message.text:
        await bot.send_message(
            ADMIN_ID,
            f"{caption}\n\n💬 Xabar:\n{message.text}",
            parse_mode='HTML'
        )
    elif message.photo:
        await bot.send_photo(
            ADMIN_ID,
            photo=message.photo[-1].file_id,
            caption=caption
        )
    elif message.video:
        await bot.send_video(
            ADMIN_ID,
            video=message.video.file_id,
            caption=caption
        )
    elif message.document:
        await bot.send_document(
            ADMIN_ID,
            document=message.document.file_id,
            caption=caption
        )
    elif message.voice:
        await bot.send_voice(
            ADMIN_ID,
            voice=message.voice.file_id
        )
        await bot.send_message(ADMIN_ID, caption, parse_mode='HTML')
    elif message.audio:
        await bot.send_audio(
            ADMIN_ID,
            audio=message.audio.file_id
        )
        await bot.send_message(ADMIN_ID, caption, parse_mode='HTML')
    
    await message.answer("✅ Xabaringiz qabul qilindi. Javob kutib turing.")


# ==================== STARTUP ====================

async def main():
    """Main function"""
    logger.info("🤖 Bot ishga tushmoqda...")
    try:
        await dp.start_polling(bot)
    except KeyboardInterrupt:
        logger.info("❌ Bot to'xtatildi")
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
