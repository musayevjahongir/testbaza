#bot.py fayli kodi
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import handlers

def main():
    TOKEN = "7099265445:AAHwc-D2btRm_91n27KeG4qafkpZT8ORC30"

    updater = Updater(TOKEN)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', handlers.start))
    dp.add_handler(CallbackQueryHandler(handlers.admin, pattern='admin stng'))
    dp.add_handler(CallbackQueryHandler(handlers.userfun, pattern='user obuna'))
    dp.add_handler(CallbackQueryHandler(handlers.admin_control,pattern='admin '))
    dp.add_handler(CallbackQueryHandler(handlers.teststng,pattern='answer '))
    dp.add_handler(CallbackQueryHandler(handlers.test,pattern='test '))
    dp.add_handler(CallbackQueryHandler(handlers.balltest,pattern='ball +'))
    dp.add_handler(MessageHandler(Filters.regex(r'^admin\+'),handlers.addadmin))
    dp.add_handler(MessageHandler(Filters.regex(r'^admin\-'),handlers.deladmin))
    dp.add_handler(MessageHandler(Filters.regex(r'^obuna\+'),handlers.add_obuna))
    dp.add_handler(MessageHandler(Filters.regex(r'^obuna\-'),handlers.del_obuna))
    dp.add_handler(MessageHandler(Filters.regex(r'^test\+'),handlers.addtest))
    dp.add_handler(MessageHandler(Filters.regex(r'send'),handlers.reklama))
    dp.add_handler(MessageHandler(Filters.regex(r'$'),handlers.check_answer))





    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

#handlers.py fayli kodlari
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from telegram.ext import CallbackContext
import keyboards
import db
import sqlite3
from datetime import datetime 
import pytz


def start(update: Update, context: CallbackContext):
    username = update.message.chat.username
    chat_id = update.message.chat_id
    
    if db.check_admin(username):
        update.message.reply_text(
            text = "Assalomu alaykum botga xush kelibsiz, bo'limlardan birini tanlang.",
            reply_markup=keyboards.start_admin()
        )
    else:
        if not db.check_user(chat_id):
            db.add_user(chat_id)
        channel=db.get_channel()
        btn=[]
        for chnl in channel:
            chat = context.bot.get_chat(chnl[0])
            channel_name = chat.title
            btn.append([InlineKeyboardButton(channel_name,callback_data='obuna',url=f'https://t.me/{chnl[0][1:]}')])
        btn.append([InlineKeyboardButton('✅Azo Boʻldim✅',callback_data='user obuna')])
        btn = InlineKeyboardMarkup(btn)
        update.message.reply_text(
            text = f"Assalomu alaykum {update.message.from_user.first_name}.\nBotdan foydalanish uchun quyidagi kanallarga a'zo bo'ling 👇",
            reply_markup=btn
        )      
def admin(update: Update, context: CallbackContext):
    update.callback_query.message.reply_text(
        text="Bo'limlardan birini tanlang👇",
        reply_markup=keyboards.admin()
    )

def check(chat_id,bot,channels):
    for channel in channels:
        chan1=bot.getChatMember(channel[0],str(chat_id))['status']
        if chan1=='left':
            return False
    return True

def userfun(update: Update, context: CallbackContext):
    query=update.callback_query
    chat_id=query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    channel=db.get_channel()
    a=check(chat_id, bot, channel)
    if a:
        update.callback_query.message.reply_text(
        text="Obuna mufavaqiyatli amalga oshirildi!\nBo'limlardan birini tanlang👇.",
        reply_markup=keyboards.userfun())
    else:
        bot.sendMessage(chat_id,'Obuna bo\'lishda xatolik!')
    bot.delete_message(chat_id,msg)

def admin_control(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    b = query.data.split(' ')[1]
    if b=='admin+':
        text = "Yangi admin qo'shish uchun\n```admin+user_name```\nKo'rinishida yangi adminni yuboring."
        bot.sendMessage(chat_id,text, parse_mode=ParseMode.MARKDOWN)
        bot.delete_message(chat_id, msg)
    elif b=='admin-':
        text = "Adminlikdan olish uchun\n```admin-user_name```\nKo'rinishida o'chirilishi kerak bo'lgan admin user_nameni yuboring."
        bot.sendMessage(chat_id,text)
        bot.delete_message(chat_id, msg)
    elif b == 'obuna':
        text = "Majburiy obuna qo'shish uchun avval botni kanal(guruh)ga to'liq admin qilasiz va quyidagicha ulaysiz:\n```obuna+@username```\n\nAksincha kanalni majburiy obunadan olib tashlash uchun:\n```obuna-@username```"
        bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
    elif b=='msg':
        text = "Foydalanuvchilarga xabar jo'natish uchun yubormoqchi bo'lgan xabaringizga *send* so'zini reply qilib yozing"
        bot.sendMessage(chat_id,text,parse_mode=ParseMode.MARKDOWN)
    elif b == 'stc':
        res = len(db.get_users())
        text = f"Botdagi foydalanuvchilar umumiy soni: {res}"
        bot.sendMessage(chat_id,text)
    elif b=='adminlar':
        asoni=len(db.get_admins())
        text = f"Botdagi adminlar soni: {asoni}"
        bot.sendMessage(chat_id, text)
        bot.delete_message(chat_id, msg)
def addadmin(update: Update, context: CallbackContext):
    username = update.message.chat.username
    chat_id=update.message.chat_id
    bot=context.bot
    if db.check_admin(username):
        user_id = update.message.text[6:]
        if not db.check_admin(user_id):
            db.add_admin(user_id)
            bot.send_message( chat_id,'Admin qo\'shildi✅')
        else:
            bot.send_message( chat_id,'Bunday admin oldindan bor')
    else:
        bot.send_message( chat_id,'Admin qo\'shish uchun siz ham admin bo\'lishingiz kerak')
def deladmin(update: Update, context: CallbackContext):
    username = update.message.chat.username
    chat_id=update.message.chat_id
    bot=context.bot
    if db.check_admin(username):
        user_id = update.message.text[6:]
        if db.check_admin(user_id):
            db.del_admin(user_id)
            bot.send_message(chat_id,'Admin o\'chirildi✅')
        else:
            bot.send_message( chat_id,'Bunday admin yo\'q')
    else:
        bot.send_message( chat_id,'Admin o\'chirish uchun siz ham admin bo\'lishingiz kerak')

def add_obuna(update: Update, context: CallbackContext):
    username = update.message.chat.username
    chat_id = update.message.chat_id
    bot = context.bot
    if db.check_admin(username):
        user_id = update.message.text[6:]
        if not db.check_chennel(user_id):
            db.add_channel(user_id)
            bot.send_message( chat_id,'Majburiy obuna qo\'shildi✅')
        else:
            bot.send_message( chat_id,'Bunday obuna oldindan bor')
    else:
        bot.send_message( chat_id,'Obuna qo\'shish uchun siz admin bo\'lishingiz kerak')

def del_obuna(update: Update, context: CallbackContext):
    username = update.message.chat.username
    chat_id = update.message.chat_id
    bot = context.bot
    if db.check_admin(username):
        user_id = update.message.text[6:]
        if db.check_chennel(user_id):
            db.del_obuna(user_id)
            bot.send_message( chat_id,'Majburiy obuna o\'chirildi✅')
        else:
            bot.send_message( chat_id,'Bunday obuna yo\'q')
    else:
        bot.send_message( chat_id,'Obuna o\'chirish uchun siz admin bo\'lishingiz kerak')

def test(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    b = query.data.split(' ')[1]
    if b=='+':
        text = """
👇👇👇 Yo'riqnoma✅

👇Test yaratish uchun:

test+Ism familiya*Fan nomi*to'g'ri javoblar 

ko`rinishida yuboring‼️

👇Misol:
 
test+Aliyev Ali*Matematika*abbccdd...*#  
yoki
test+Aliyev Ali*Matematika*1a2d3c4a5b...*#
        """
        btn=InlineKeyboardButton('Ballik test yaratish✅',callback_data='ball +')
        btn = InlineKeyboardMarkup([[btn]])
        bot.send_message(chat_id,text)
    else:
        text = """
👇👇👇 Yo'riqnoma✅

👇Test javoblarini yuborish uchun ‼️

test kodi*Ism familiya*abbccdd... 
yoki
test kodi*Ism familiya*1a2d3c4a5b...

kabi ko`rinishlarda yuboring✅

👇Misol: 

$1234*Aliyev Ali*abbccdd... 
yoki
$1234*Aliyev Ali*1a2d3c4a5b...
        """
        bot.send_message(chat_id,text)
def reklama(update:Update, context:CallbackContext):
    org_msg=update.message.reply_to_message
    text=update.message.text
    bot=context.bot
    chat_id=update.message.chat_id
    username=update.message.chat.username
    if db.check_admin(username):
        if text=='send':
            users=db.get_users()
            i=0
            for user in users:
                context.bot.forward_message(chat_id=user[0], from_chat_id=org_msg.chat_id, message_id=org_msg.message_id)
                i+=1
            
            bot.send_message(chat_id,f'{i} ta foydalanuvchiga xabar yuborildi')
    else:
        bot.send_message(chat_id, "Reklama jo'natish uchun admin bo'lishingiz kerak!!")

def addtest(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    username = update.message.chat
    data = update.message.text
    command = f"""
     SELECT name FROM Obuna
    """
    channel = cr.execute(command).fetchall()
    a = check(chat_id,bot,channel)
    command = f"""
        SELECT * FROM Admins WHERE username = "{username}"
    """
    admin = cr.execute(command).fetchall()
    cnt.commit()
    if (a or admin):
        try:
            a1,a,b,h=data[5:].split('*')
            if len(a1)>37:
                bot.sendMessage(chat_id,'Ism familya uchun matn uzun')
                return 0
            if b[0]!='1':
                t1 = b
            else:
                t1 = ''.join([char for char in b if char.isalpha()])
            if h[0]!='#':
                try:
                    h1 = h.split(';')
                    if len(h1)!=len(t1):
                        bot.send_message(chat_id,'❗️❗️❗️Testga ball qo\'shishda qandaydir xatolik. Qo\'llanmani qayta o\'qib ko\'rib qayta urining.')
                        return 0
                    else:
                        h1=sum(float(x0) for x0 in h1)
                        h1=round(h1,1)
                except:
                    bot.send_message(chat_id,'❗️❗️❗️Testga ball qo\'shish qismida qandaydir xatolik. Qo\'llanmani qayta o\'qib ko\'rib qayta urining.')
                    return 0
            else:
                h1=len(t1)
            cnt = sqlite3.connect('data.db')
            cr = cnt.cursor()
            command = f"""
            INSERT INTO Tests (name,chat_id,subject,test,rate) VALUES ("{a1}","{chat_id}","{a}","{t1}","{h}")
            """
            cr.execute(command)
            text = f"""
✅Test bazaga qo'shildi.

Test kodi: ${cr.lastrowid}
Savollar soni: {len(t1)} ta
Umumiy ball: {h1} ball

Testda qatnashuvchilar quyidagi ko'rinishda javob yuborishlari mumkin:

${cr.lastrowid}*Ism Familya*abcde... ({len(t1)} ta) 
yoki
${cr.lastrowid}*Ism Familya*1a2b3c4d5e... ({len(t1)} ta)
            """
            cnt.commit()
            btn1 = InlineKeyboardButton('Joriy holat',callback_data=f'answer 1{cr.lastrowid}')
            btn2 = InlineKeyboardButton('Yakunlash',callback_data=f'answer 2{cr.lastrowid}')
            btn = InlineKeyboardMarkup([[btn1,btn2]])
            bot.send_message(chat_id,text,reply_markup=btn)
        except:
            bot.send_message(chat_id,'❗️❗️❗️Qandaydir xatolik qayta tekshirib urinib ko\'ring')
    else:
        text = "❗️❗️❗️\n\nMajburiy obunani amalga oshirmasdan botdan foydalana olmaysiz."
        chat = context.bot.get_chat(channel)
        channel_name = chat.title
        btn1 = InlineKeyboardButton(channel_name,callback_data='obuna',url=f'https://t.me/{channel[1:]}')
        btn2 = InlineKeyboardButton('✅Azo Boʻldim✅',callback_data='user obuna')
        btn = InlineKeyboardMarkup([[btn1],[btn2]])
        bot.sendMessage(chat_id,text,reply_markup=btn)

def check_answer(update:Update, context:CallbackContext):
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    bot=context.bot
    chat_id = update.message.chat_id
    username = update.message.chat.username
    command = f"""
     SELECT name FROM Obuna
    """
    channel = cr.execute(command).fetchall()
    a = check(chat_id,bot,channel)
    command = f"""
        SELECT * FROM Admins WHERE username = "{username}"
    """
    admin = cr.execute(command).fetchall()
    cnt.commit()
    if (a or admin):
        try:
            cnt = sqlite3.connect('data.db')
            cr = cnt.cursor()
            data = update.message.text
            a,b,c = data[1:].split('*')
            c= ''.join([char for char in c if char.isalpha()])
            command = f"""
            SELECT * FROM Tests WHERE id={a}
            """
            ch = cr.execute(command).fetchall()
            if ch:
                test1 = ch[0][-2]
                if len(test1) != len(c):
                    bot.send_message(chat_id,f'Savollar soni {len(test1)} ta, javoblar bilan mutonosibmas!')
                    return 0
                if len(b)>35:
                    bot.sendMessage(chat_id,'Ism familya uchun matn uzun!')
                    return 0
                command = f"""
                SELECT * FROM Answer WHERE id={a} AND chat_id="{chat_id}"
                """
                ch1 = cr.execute(command).fetchall()
                if ch1:
                    bot.sendMessage(chat_id,'❗️❗️❗️Siz oldinroq bu testga javob yuborgansiz.\n\nBitta testga faqat bir marta javob yuborish mumkin!')
                    return 0
                k=0
                p=1
                xatolar = '!'
                if ch[0][-1]=='#':
                    for i,j in zip(c,test1):
                        if i == j:
                            k+=1
                        else:
                            xatolar += f'{p},'
                        p+=1
                    rate = k
                else:
                    rate = 0
                    r = ch[0][-1].split(';')
                    for i,j,l in zip(c,test1,r):
                        if i == j:
                            k+=1
                            rate+=float(l)
                        else:
                            xatolar += f'{p},'
                        p+=1
                    rate=round(rate,1)
                # pr=round((k/(len(test1)/2))*100,1)
                
                command = f"""
                INSERT INTO Answer VALUES ({a},"{b}","{chat_id}",{k},{rate},"{xatolar}")
                """
                cr.execute(command)
                cnt.commit()
                hozirgi_vaqt = datetime.now()


                toshkent_vaqti = pytz.timezone('Asia/Tashkent')
                hozirgi_vaqt_toshkent = hozirgi_vaqt.astimezone(toshkent_vaqti)
                text = f"""
👤 Foydalanuvchi: 
{b}
📚 Fan: {ch[0][3]}
📖 Test kodi: ${a}
✏️ Jami savollar soni: {len(test1)} ta
✅ To'g'ri javoblar soni: {k} ta
📊 To'plangan ball: {rate} ball
🔣 Foiz : {round((k/len(test1))*100,1)} %
--------------------------------
🕐 Sana, vaqt: {hozirgi_vaqt_toshkent.strftime("%Y-%m-%d %H:%M:%S")}
                """
                bot.send_message(chat_id,text)
            else:
                bot.send_message(chat_id,"❗️❗️❗️\nTest vaqti yakunlangan yoki noto'g'ri test kodi")
        except:
            bot.send_message(chat_id,'❗️❗️❗️Qandaydir xatolik qayta tekshirib urinib ko\'ring')

    else:
        text = "❗️❗️❗️\n\nMajburiy obunani amalga oshirmasdan botdan foydalana olmaysiz."
        btn1 = InlineKeyboardButton('➕Kanalga Oʻtish✅',callback_data='obuna',url=f'https://t.me/{channel[1:]}')
        btn2 = InlineKeyboardButton('✅Azo Boʻldim✅',callback_data='user obuna')
        btn = InlineKeyboardMarkup([[btn1],[btn2]])
        bot.sendMessage(chat_id,text,reply_markup=btn)


def teststng(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    b = query.data.split(' ')[1]
    cnt = sqlite3.connect('data.db')
    cr = cnt.cursor()
    if b[0]=='1':
        command = f"""
        SELECT * FROM Answer
        WHERE id = {b[1:]}
        ORDER BY marks DESC;
        """
        asw = cr.execute(command).fetchall()
        if asw:
            command = f"""
            SELECT * FROM Tests WHERE id = {b[1:]}
            """
            anw = cr.execute(command).fetchall()
            if anw[0][-1]!='#':
                marks = anw[0][-1].split(';')
                h1=sum(float(x0) for x0 in marks)
                h1=round(h1,1)
            else:
                h1=(len(anw[0][-2]))
            text = f"""
Test holati.

Fan: {anw[0][3]}
Test kodi: ${b[1:]}
Savollar soni: {len(anw[0][-2])} ta
Maksimal ball: {h1} ball

Natijalar:
"""
            k=1
            for i in asw:
                text+=f"{k}) {i[1]} - {i[-2]} ball\n"
                k+=1
            bot.sendMessage(chat_id,text)

    else:
        command = f"""
        SELECT * FROM Tests WHERE id = {b[1:]}
        """
        anw = cr.execute(command).fetchall()
        if anw[0][-1]!='#':
            marks = anw[0][-1].split(';')
            h1=sum(float(x0) for x0 in marks)
            h1=round(h1,1)
        else:
            h1=len(anw[0][-2])
        text1 = '\nTo\'g\'ri javoblar:\n'
        q=1
        lenth=len(anw[0][-2])
        for m in anw[0][-2]:
            text1 += f"{q}.{m} "
            q+=1
        text = f"""
#Natijalar_${b[1:]}
#{anw[0][3]}
        
🔐Test yakunlandi.

Fan: {anw[0][3]}
Test kodi: ${b[1:]}
Savollar soni: {lenth} ta
Maksimal ball: {h1} ball

✅ Natijalar:

"""

        command = f"""
        SELECT * FROM Answer
        WHERE id = {b[1:]}
        ORDER BY marks DESC;
        """
        asw = cr.execute(command).fetchall()
        command = f"""
        SELECT DISTINCT marks FROM Answer WHERE id={b[1:]} ORDER BY marks DESC LIMIT 3
        """
        asnw = cr.execute(command).fetchall()
        if asw:
            k=1
            medal = {'a':'🥇','b':'🥈','c':'🥉'}
            for i in asw:
                text2 = f'☝️ Diqqat!\n⛔️ Test yakunlandi.\nTest kodi: ${b[1:]}\nFan nomi:{anw[0][3]}\n\n'
                text+=f"{k}) {i[1]} - {i[-2]} ball\n"
                if i[-1]!='!':
                    text2+=f'❌ Sizning noto\'g\'ri javoblaringiz:\n[{i[-1][1:]}]'
                else:
                    text2+='Sizda barcha javoblar to\'gri'
                k+=1
                bot.send_message(i[2],text2)
            text = text + '' + text1 + "\n\nTestda qatnashgan barcha ishtirokchilarga minnatdorchilik bildiramiz. Bilimingiz ziyoda bo’lsin!!☺️"
            bot.deleteMessage(chat_id,msg)
            bot.sendMessage(chat_id, text)
            y=0
            names=[[],[],[]]
            mks = []
            cont = []
            for qw in asnw:
                command = f"""
                SELECT * FROM Answer WHERE marks = {qw[0]} AND id = {b[1:]}
                """
                qwe = cr.execute(command).fetchall()
                cont.append(qwe[0][-3])
                for nm in qwe:
                    names[y].append(nm[1])
                y+=1
                mks.append(round((float(qwe[0][-3])/int(lenth))*100,1))

            command = f"""
            DELETE FROM Answer WHERE id = {b[1:]}
            """
            cr.execute(command)
            command = f"""
            DELETE FROM Tests WHERE id = {b[1:]}
            """
            cr.execute(command)
            cnt.commit()
        else:
            bot.deleteMessage(chat_id,msg)
            text = text+text1+'\n\nTestda hech kim ishtirok etmadi!'
            bot.sendMessage(chat_id, text=text)
            

def balltest(update:Update, context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    msg = query.message.message_id
    bot=context.bot
    text = """
👇👇👇 Yo'riqnoma✅

👇Ballik test yaratish uchun:

test+Ism familiya*Fan nomi*to'g'ri javoblar*ball

ko`rinishida yuboring‼️

👇Misol  uchun:
 
test+Aliyev Ali*Matematika*abbc...*1.3;2.2;2.2;1.3;...  
yoki
test+Aliyev Ali*Matematika*1a2d3c4a...*1.3;2.2;2.2;1.3;...

❗️❗️ ball - har bir testga ball qo'shish uchun ishlatiladi buni to'ldirish quyidagicha:
✅1.3;2.2;2.2;... ko'rinishida ballarni yuboring.

✅o'nli kasrni . bilan bering, orasi ; bilan bering, oxiriga ; qo'ymang

✅Barcha test uchun ball kiriting.

❗️Agar testga ball qo'shishni xoxlamsangiz ball qismiga shunchaki # belgisini qo'shish kifoya (bu xolatda har bir test 1 balldan hisoblanadi)
"""
    bot.deleteMessage(chat_id,msg)
    bot.sendMessage(chat_id,text)

#db.py fayli kodi
import sqlite3
def get_admins():
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute("SELECT username FROM Admins")
    chat_ids = cursor.fetchall()
    cnt.close()
    return chat_ids
def add_admin(username:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""INSERT INTO Admins (username) VALUES ("{username}")""")
    cnt.commit()
    cnt.close()
    return True
def del_admin(username:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""DELETE FROM Admins WHERE username = ("{username}")""")
    cnt.commit()
    cnt.close()
    return True
def del_user(chat_id:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""DELETE FROM Users WHERE chat_id = ("{chat_id}")""")
    cnt.commit()
    cnt.close()
    return True

def get_channel():
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute("SELECT name FROM Obuna")
    channels = cursor.fetchall()
    cnt.close()
    return channels

def check_chennel(chat_id: str)->list:
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""SELECT * FROM Obuna WHERE name = ("{chat_id}")""")
    a=cursor.fetchall()
    cnt.close()
    return a

def get_users():
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute("SELECT chat_id FROM Users")
    chat_ids = cursor.fetchall()
    cnt.close()
    return chat_ids
def add_channel(name:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""INSERT INTO Obuna (name) VALUES ("{name}")""")
    cnt.commit()
    chat_ids = cursor.fetchall()
    cnt.close()
    return chat_ids

def del_obuna(name:str):
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""DELETE FROM Obuna WHERE name = ("{name}")""")
    cnt.commit()
    chat_ids = cursor.fetchall()
    cnt.close()
    return chat_ids

def add_user(chat_id: str)->bool:
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f"""INSERT INTO Users (chat_id) VALUES ("{chat_id}")""")
    cnt.commit()
    cnt.close()
    return True
def check_admin(username: str)->list:
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f'SELECT * FROM Admins WHERE username = "{username}"')
    a=cursor.fetchall()
    print(username)
    cnt.close()
    return a
def check_user(chat_id: str)->list:
    cnt = sqlite3.connect('data.db')
    cursor = cnt.cursor()
    cursor.execute(f'SELECT * FROM Users WHERE chat_id = "{chat_id}"')
    a=cursor.fetchall()
    cnt.close()
    return a

#requirements.txt fayli
"""anyio==4.3.0
certifi==2024.2.2
h11==0.14.0
httpcore==1.0.5
httpx==0.27.0
idna==3.6
python-telegram-bot==13.15
sniffio==1.3.1
tinydb==4.8.0"""
#keyboards.py fayli kodi
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import db
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

shu kodni flaskka qoyib ber 