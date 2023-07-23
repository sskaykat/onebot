import telebot
import qrcode 
import base64
import os

API_KEY = os.environ.get('API_KEY', "")
bot = telebot.TeleBot(API_KEY)
# bot = telebot.TeleBot('6058236364:AAHlMLUhcETG6VdZhCg57PIzX7PcTjDe8NQ')


# /start命令处理函数
@bot.message_handler(commands=['start'])  
def handle_start(message):
    bot.send_message(message.chat.id, "欢迎使用!!!")

# 文本消息处理函数
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == '/qrcode':
        bot.send_message(message.chat.id, "请回复要转换成二维码的文本内容:")
        bot.register_next_step_handler(message, generate_qrcode)
    elif message.text == '/base64':
        bot.send_message(message.chat.id, "请回复要Base64编码的文本内容:")
        bot.register_next_step_handler(message, encode_base64)
    elif message.text == '/base64jm':
        bot.send_message(message.chat.id, "请回复要解码的Base64文本内容:")
        bot.register_next_step_handler(message, decode_base64)

# 生成二维码
def generate_qrcode(message):
    text = message.text
    img = qrcode.make(text)
    img.save('qrcode.png') 
    photo = open('qrcode.png', 'rb')
    bot.send_photo(message.chat.id, photo)

# Base64编码处理函数  
def encode_base64(message):
    text = message.text
    text_bytes = text.encode('utf-8')
    base64_bytes = base64.b64encode(text_bytes)
    base64_text = base64_bytes.decode('ascii')
    
    bot.send_message(message.chat.id, base64_text) 

# Base64解码处理函数
def decode_base64(message):
    base64_text = message.text
    base64_bytes = base64_text.encode('utf-8')
    text_bytes = base64.b64decode(base64_bytes)
    text = text_bytes.decode('utf-8')
    
    bot.send_message(message.chat.id, text) 

bot.polling()
