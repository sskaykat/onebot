import telebot
import qrcode 
import base64
import os
import random
import string
import uuid
import requests

API_KEY = os.environ.get('API_KEY', "")
bot = telebot.TeleBot(API_KEY)
# bot = telebot.TeleBot('6058236**********TjDe8NQ')

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
    elif message.text == '/base64decoding':
        bot.send_message(message.chat.id, "请回复要解码的Base64文本内容:")
        bot.register_next_step_handler(message, decode_base64)
    elif message.text == '/randompassword':
        bot.send_message(message.chat.id, generate_random_password())
    elif message.text == '/uuid':
        bot.send_message(message.chat.id, generate_uuid())
    elif message.text == '/bingwallpaper':
        download_bing_wallpaper(message.chat.id)


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
    base64_bytes = base64_text.encode('ascii')
    text_bytes = base64.b64decode(base64_bytes)
    text = text_bytes.decode('utf-8')
    
    bot.send_message(message.chat.id, text) 

# 生成随机密码
def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(12))
    return password

# 生成UUID
def generate_uuid():
    return str(uuid.uuid4())
    
# 下载必应每日壁纸
def download_bing_wallpaper(chat_id):
    # 构建必应每日壁纸的URL
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'

    try:
        # 发送GET请求获取必应每日壁纸信息
        response = requests.get(url)
        data = response.json()

        # 提取壁纸的相对路径
        wallpaper_path = data['images'][0]['url']

        # 构建完整的壁纸URL
        wallpaper_url = 'https://www.bing.com' + wallpaper_path

        # 发送GET请求下载壁纸
        wallpaper_response = requests.get(wallpaper_url)

        # 保存壁纸文件
        with open('bing_wallpaper.jpg', 'wb') as f:
            f.write(wallpaper_response.content)

        # 发送壁纸给用户
        photo = open('bing_wallpaper.jpg', 'rb')
        bot.send_photo(chat_id, photo)

        # 删除下载的壁纸文件
        os.remove('bing_wallpaper.jpg')

    except Exception as e:
        bot.send_message(chat_id, '下载壁纸时发生错误。')



bot.polling()
