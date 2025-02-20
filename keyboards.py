from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def start_admin():
    btn1 = InlineKeyboardButton('Statistika',callback_data=f'admin stc')
    btn2 = InlineKeyboardButton('Admin⚙️',callback_data='admin stng')
    btn3 = InlineKeyboardButton('Majburiy obuna',callback_data='admin obuna')
    btn4 = InlineKeyboardButton('Xabar yuborish',callback_data='admin msg')
    btn6 = InlineKeyboardButton("➕Test yaratish",callback_data='test +')
    btn7 = InlineKeyboardButton("✅Javobni tekshirish",callback_data='test tek')
    return InlineKeyboardMarkup([[btn2,btn1], [btn3,btn4],[btn6,btn7]])

def admin():
    btn1 = InlineKeyboardButton("Admin qo'shish", callback_data='admin admin+')
    btn2 = InlineKeyboardButton("Admin olish", callback_data='admin admin-')
    btn3 = InlineKeyboardButton("Adminlarni ko'rish", callback_data='admin adminlar')
    return InlineKeyboardMarkup([[btn1], [btn2], [btn3]])
def userfun():
    btn1 = InlineKeyboardButton("➕Test yaratish",callback_data='test +')
    btn2 = InlineKeyboardButton("✅Javobni tekshirish",callback_data='test tek')
    return InlineKeyboardMarkup([[btn1],[btn2]])

