import telebot
import qrcode 
import base64
import config

API_KEY = os.environ.get('API_KEY', "")
bot = telebot.TeleBot(API_KEY)

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
    text_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(text_bytes)
    base64_text = base64_bytes.decode('ascii')
    
    bot.send_message(message.chat.id, base64_text) 

bot.polling()
