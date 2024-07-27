import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot('7331998507:AAGPULwRv13Qx8PSQNxh9o8CJfX-ImfFHk4')
name = None
role =''
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Зарегистрироваться',callback_data='reg')
    btn2 = types.InlineKeyboardButton('Авторизоваться',callback_data='auth')
    btn3 = types.InlineKeyboardButton('Установить роль',callback_data='role')
    
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Привет, выбери команду!', reply_markup=markup)
    
    
@bot.callback_query_handler(func = lambda call: call.data == 'reg')
def register(call):
    conn = sqlite3.connect('mybase2.db')
    cur = conn.cursor()
    
    cur.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(50), pass varchar(50), role TEXT DEFAULT "user")')
    conn.commit()
    cur.close()
    conn.close()
    
    bot.send_message(call.message.chat.id,'Привет, сейчас тебя зарегистрируем! Введи имя: ')
    bot.register_next_step_handler(call.message,user_name) 

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id,'Введи пароль: ')
    bot.register_next_step_handler(message,user_psw)

def user_psw(message):
    password = message.text.strip()  

    conn = sqlite3.connect('mybase2.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()   
    for el in users:
        if name == el[1]:
            bot.send_message(message.chat.id,'Такой пользователь уже существует')
            bot.register_next_step_handler(message,start)
            break
    else:    
        cur.execute('INSERT INTO users (name,pass,role) VALUES ("%s","%s","%s")'% (name,password,'user'))
        conn.commit()
        cur.close()
        conn.close()    
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Авторизоваться',callback_data='auth'))
        bot.send_message(message.chat.id, 'Пользователь зарегистрирован!',reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Авторизоваться')    
def auth_request(message):
    bot.send_message(message.chat.id, 'Введите Логин: ')
    bot.register_next_step_handler(message, get_login)

@bot.callback_query_handler(func = lambda call: call.data == 'auth')
def auth(call):
    bot.send_message(call.message.chat.id,'Введите Логин: ')
    bot.register_next_step_handler(call.message, get_login)
    
def get_login(message):
    global login
    login = message.text.strip()
    bot.send_message(message.chat.id,'Введите пароль: ')
    bot.register_next_step_handler(message, get_pass)
    
def get_pass(message):
    password = message.text.strip()
    
    conn = sqlite3.connect('mybase2.db')
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()    
    global role
    flag = False
    for el in users:
        if login==el[1] and password==el[2]:
            flag = True
            role = el[3]            
            break
        print(el)
    print(role,flag)   
    if flag == True:       
        bot.send_message(message.chat.id,'Авторизация успешна')
        if role == 'admin':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Список пользователей',callback_data='role'))
            markup.add(types.InlineKeyboardButton('Профиль',callback_data='profile'))
            bot.send_message(message.chat.id,'Здраствуй Администратор',reply_markup=markup)
        elif role == 'user':
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Профиль',callback_data='profile'))
            bot.send_message(message.chat.id,'Здраствуй пользователь',reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Неверные данные или пользователь не зарегистрирован ! Введите команду /start и попробуйте заново.')        
        bot.register_next_step_handler(message, start)
        
    cur.close()
    conn.close()

@bot.callback_query_handler(func = lambda call: call.data == 'role')
def callback(call):
    conn = sqlite3.connect('mybase2.db')
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    
    info =''
    for el in users:
        info+= f'Имя {el[1]} - Роль {el[3]}\n'
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id,info)

@bot.callback_query_handler(func = lambda call: call.data == 'profile')
def callback(call):
    conn = sqlite3.connect('mybase2.db')
    cur = conn.cursor()
    
    cur.execute('SELECT * FROM users WHERE name = ?',(login,))
    users = cur.fetchall()
    
    info =''
    for el in users:
        info+= f'Имя {el[1]} - Роль {el[3]}\n'
    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id,info)
    
bot.polling(none_stop=True)










# @bot.callback_query_handler(func = lambda call: True)
# def callback(call):
#     conn = sqlite3.connect('mybase.db')
#     cur = conn.cursor()
    
#     cur.execute('SELECT * FROM users')
#     users = cur.fetchall()
    
#     info =''
#     for el in users:
#         info+= f'Имя {el[1]}\n'
#     cur.close()
#     conn.close()
#     bot.send_message(call.message.chat.id,info)
