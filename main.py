import os
import telebot
import pandas as pd
import pymongo
from telebot import types
from threading import Thread
from flask import Flask

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive and running safely with MongoDB!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# Environment Variables များကို ယူခြင်း
BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_CHAT_ID = int(os.environ.get('ADMIN_CHAT_ID', '0'))
MONGO_URI = os.environ.get('MONGO_URI')

# 💡 ဖြေရှင်းချက် (၁) - MongoDB လိုင်းပိတ်ပြီး Hang မနေစေရန် Timeout (၅ စက္ကန့်) သတ်မှတ်ခြင်း
client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
db = client['student_database']
collection = db['students_records']

bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}
TEMP_EXCEL_FILE = "students_data.xlsx"

# /start သို့မဟုတ် \start မဟုတ်ဘဲ အလွတ်ဝင်လာသူများကို ကြိုဆိုစာပြခြင်း
@bot.message_handler(func=lambda message: message.text not in ['/start', '\\start', '/download'] and message.chat.id not in user_data)
def welcome_message(message):
    bot.send_message(
        message.chat.id, 
        "ကျောင်းသားအချက်အလက်စုဆောင်းရေး Bot မှ ကြိုဆိုပါတယ်။\n\nစတင်ရန်အတွက် **\\start** ကို ရိုက်ထည့်ပေးပါ။",
        parse_mode="Markdown"
    )

# Form สတင်ခြင်း
@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == '\\start')
def start_form(message):
    chat_id = message.chat.id
    
    # 💡 ဖြေရှင်းချက် (၂) - နောက်ကွယ်တွင် ရှုပ်ထွေးမနေစေရန် ယခင်ကျန်ခဲ့သော Form အဆင့်ဟောင်းများကို လုံးဝအပြီးတိုင် ဖျက်ပစ်ခြင်း
    bot.clear_step_handler_by_chat_id(chat_id)
    
    user_data[chat_id] = {}
    msg = bot.send_message(chat_id, "⚙️ စတင်ရန်အတွက် သင်၏ **ကျောင်းသား ID** (ဥပမာ - KPTMYK-00____) ကို ရိုက်ထည့်ပေးပါရန်။")
    bot.register_next_step_handler(msg, process_student_id)

def process_student_id(message):
    chat_id = message.chat.id
    user_data[chat_id]['student_id'] = message.text
    msg = bot.send_message(chat_id, "သင်၏ **ကျောင်းသားအမည်** ကို ရိုက်ထည့်ပေးပါရန်။")
    bot.register_next_step_handler(msg, process_student_name)

def process_student_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['student_name'] = message.text
    msg = bot.send_message(chat_id, "သင်၏ **၁၀တန်းအောင်ခုနှစ်** (20__-20__)ကို ရိုက်ထည့်ပေးပါရန်။")
    bot.register_next_step_handler(msg, process_passing_year)

def process_passing_year(message):
    chat_id = message.chat.id
    user_data[chat_id]['passing_year'] = message.text
    msg = bot.send_message(chat_id, "စာမေးပွဲဖြေဆိုခဲ့သည့် **စာမေးပွဲဌာန** ကို ရိုက်ထည့်ပေးပါရန်။")
    bot.register_next_step_handler(msg, process_exam_center)

def process_exam_center(message):
    chat_id = message.chat.id
    user_data[chat_id]['exam_center'] = message.text
    msg = bot.send_message(chat_id, "သင်၏ **၁၀တန်းခုံအမှတ်** ကို ရိုက်ထည့်ပေးပါရန်။")
    bot.register_next_step_handler(msg, process_matric_roll)

def process_matric_roll(message):
    chat_id = message.chat.id
    user_data[chat_id]['matric_roll'] = message.text
    msg = bot.send_message(chat_id, "**အုပ်ထိန်းသူ ဖုန်းနံပါတ်** ကို ရိုက်ထည့်ပေးပါရန်။")
    bot.register_next_step_handler(msg, process_phone)

def process_phone(message):
    chat_id = message.chat.id
    user_data[chat_id]['phone'] = message.text
    msg = bot.send_message(chat_id, "သင်ရရှိခဲ့သော **ဘာသာစုံအမှတ်ပေါင်း** ကို ရိုက်ထည့်ပေးပါရန်။")
    bot.register_next_step_handler(msg, process_total_marks)

def process_total_marks(message):
    chat_id = message.chat.id
    user_data[chat_id]['total_marks'] = message.text
    msg = bot.send_message(chat_id, "📘 **English** ဘာသာရပ်အမှတ်ကို ရိုက်ထည့်ပေးပါ။")
    bot.register_next_step_handler(msg, process_eng)

def process_eng(message):
    chat_id = message.chat.id
    user_data[chat_id]['eng'] = message.text
    msg = bot.send_message(chat_id, "📐 **Mathematics** ဘာသာရပ်အမှတ်ကို ရိုက်ထည့်ပေးပါ။")
    bot.register_next_step_handler(msg, process_math)

def process_math(message):
    chat_id = message.chat.id
    user_data[chat_id]['math'] = message.text
    msg = bot.send_message(chat_id, "⚛️ **Physics** ဘာသာရပ်အမှတ်ကို ရိုက်ထည့်ပေးပါ။")
    bot.register_next_step_handler(msg, process_phy)

def process_phy(message):
    chat_id = message.chat.id
    user_data[chat_id]['phy'] = message.text
    msg = bot.send_message(chat_id, "🧪 **Chemistry** ဘာသာရပ်အမှတ်ကို ရိုက်ထည့်ပေးပါ။")
    bot.register_next_step_handler(msg, process_preview)

def process_preview(message):
    chat_id = message.chat.id
    user_data[chat_id]['chem'] = message.text
    try:
        eng = int(user_data[chat_id]['eng'])
        math = int(user_data[chat_id]['math'])
        phy = int(user_data[chat_id]['phy'])
        chem = int(user_data[chat_id]['chem'])
        four_subjects_total = eng + math + phy + chem
        user_data[chat_id]['four_subjects_total'] = four_subjects_total
    except ValueError:
        user_data[chat_id]['four_subjects_total'] = "Error (ဂဏန်းများ မဟုတ်ပါ)"

    preview_text = (
        "🔍 **သင်ဖြည့်စွက်ထားသော အချက်အလက်များကို ပြန်လည်စစ်ဆေးပါ**\n\n"
        f"🔹 **ကျောင်းသား ID:** {user_data[chat_id]['student_id']}\n"
        f"🔹 **ကျောင်းသားအမည်:** {user_data[chat_id]['student_name']}\n"
        f"🔹 **၁၀တန်းအောင်ခုနှစ်:** {user_data[chat_id]['passing_year']}\n"
        f"🔹 **စာမေးပွဲဌာန:** {user_data[chat_id]['exam_center']}\n"
        f"🔹 **၁၀တန်းခုံအမှတ်:** {user_data[chat_id]['matric_roll']}\n"
        f"🔹 **အုပ်ထိန်းသူဖုန်း:** {user_data[chat_id]['phone']}\n"
        f"🔹 **ဘာသာစုံအမှတ်ပေါင်း:** {user_data[chat_id]['total_marks']}\n"
        f"📝 **၄ ဘာသာအမှတ်များ:** [Eng: {eng}, Math: {math}, Phy: {phy}, Chem: {chem}]\n"
        f"🧮 **၄ ဘာသာပေါင်းရလဒ်:** **{user_data[chat_id]['four_subjects_total']} မှတ်**\n\n"
        "ဖြည့်စွက်ထားသော အချက်အလက်များ အားလုံးမှန်ကန်ပါသလား?"
    )

    markup = types.InlineKeyboardMarkup()
    btn_confirm = types.InlineKeyboardButton("✅ မှန်ကန်ပါသည် (သိမ်းဆည်းမည်)", callback_data="confirm_save")
    btn_restart = types.InlineKeyboardButton("❌ မှားယွင်းနေပါသည် (အစမှပြန်ဖြည့်မည်)", callback_data="restart_form")
    markup.add(btn_confirm)
    markup.add(btn_restart)
    bot.send_message(chat_id, preview_text, reply_markup=markup, parse_mode="Markdown")

# 💡 ဖြေရှင်းချက် (၃) - ခလုတ်နှိပ်ရမည့်အဆင့်တွင် ကျောင်းသားက ခလုတ်မနှိပ်ဘဲ စာရိုက်မိပါက လမ်းညွှန်ပေးမည့် Fallback စနစ်
@bot.message_handler(func=lambda message: message.chat.id in user_data)
def preview_fallback(message):
    bot.send_message(
        message.chat.id, 
        "⚠️ ကျေးဇူးပြု၍ အပေါ်က **ခလုတ်ကို နှိပ်ပါ** သို့မဟုတ် အစမှ ပြန်စရန် **/start** ကို ရိုက်ထည့်ပေးပါရန်။",
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data:
        bot.answer_callback_query(call.id, "⚠️ သက်တမ်းကုန်ဆုံးသွားပါပြီ။ ကျေးဇူးပြု၍ /start ကို ပြန်နှိပ်ပါ။")
        return

    if call.data == "confirm_save":
        new_row = {
           
            "ကျောင်းသား ID (KPTMYK)": user_data[chat_id]['student_id'],
            "ကျောင်းသားအမည်": user_data[chat_id]['student_name'],
            "၁၀တန်းအောင်ခုနှစ်": user_data[chat_id]['passing_year'],
            "စာမေးပွဲဌာန": user_data[chat_id]['exam_center'],
            "၁၀တန်းခုံအမှတ်": user_data[chat_id]['matric_roll'],
            "အုပ်ထိန်းသူ ဖုန်းနံပါတ်": user_data[chat_id]['phone'],
            "အမှတ်ပေါင်း (စုစုပေါင်း)": user_data[chat_id]['total_marks'],
            "English": user_data[chat_id]['eng'],
            "Mathematics": user_data[chat_id]['math'],
            "Physics": user_data[chat_id]['phy'],
            "Chemistry": user_data[chat_id]['chem'],
            "၄ ဘာသာပေါင်းရလဒ်": user_data[chat_id]['four_subjects_total']
        }
        
        try:
            collection.insert_one(new_row)
            bot.edit_message_text(
                chat_id=chat_id, 
                message_id=call.message.message_id, 
                text=f"✅ သင်၏ အချက်အလက်များကို Database ထဲသို့ လုံခြုံစွာ သိမ်းဆည်းပြီးပါပြီ။\n🎯 ၄ ဘာသာပေါင်းရလဒ်: **{user_data[chat_id]['four_subjects_total']} မှတ်**\n\nကျေးဇူးတင်ပါတယ်!",
                parse_mode="Markdown"
            )
            del user_data[chat_id]
            
        except Exception as error_msg:
            bot.send_message(
                chat_id, 
                f"❌ **Database သို့ Data သိမ်းဆည်း၍ မရပါတကား!**\n\n**Error အကြောင်းရင်း:**\n`{str(error_msg)}`", 
                parse_mode="Markdown"
            )

    elif call.data == "restart_form":
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text="🔄 အချက်အလက်များကို အစမှ ပြန်လည်ဖြည့်စွက်ပေးပါ။")
        start_form(call.message)

@bot.message_handler(commands=['download'])
def download_excel(message):
    if message.chat.id == ADMIN_CHAT_ID:
        try:
            data = list(collection.find({}, {"_id": 0}))
            if data:
                df = pd.DataFrame(data)
                df.to_excel(TEMP_EXCEL_FILE, index=False)
                with open(TEMP_EXCEL_FILE, 'rb') as file:
                    bot.send_document(message.chat.id, file, caption="📊 နောက်ဆုံးရ ကျောင်းသားစာရင်း Excel File ဖြစ်ပါတယ်။")
                if os.path.exists(TEMP_EXCEL_FILE):
                    os.remove(TEMP_EXCEL_FILE)
            else:
                bot.send_message(message.chat.id, "❌ Database ထဲမှာ မည်သည့်ကျောင်းသား Data မှ မရှိသေးပါ။")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Excel ထုတ်ရာတွင် အမှားအယွင်းရှိနေပါသည်- `{str(e)}`")
    else:
        bot.send_message(message.chat.id, "🚫 သင်သည် Admin မဟုတ်ပါ။")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    print("Bot is running safely with MongoDB...")
    bot.infinity_polling()
