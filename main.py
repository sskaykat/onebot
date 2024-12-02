import telebot
from telebot import types
import qrcode
import base64
import os
import random
import string
import uuid
import requests
from PIL import Image

API_KEY = os.environ.get('API_KEY', "")
bot = telebot.TeleBot(API_KEY)
# 蓝奏云的 API URL 基础地址
API_BASE_URL = "https://v2.xxapi.cn/api/lanzou?url="

# 定义主键盘
keyboard = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
# 添加按钮到键盘
button1 = types.KeyboardButton('文本转二维码')
button2 = types.KeyboardButton('base64编码')
button3 = types.KeyboardButton('base64解码')
button4 = types.KeyboardButton('随机密码生成')
button5 = types.KeyboardButton('uuid生成器')
button6 = types.KeyboardButton('必应每日壁纸')
button7 = types.KeyboardButton('图片转ico图标')
button8 = types.KeyboardButton('舔狗日记')
button9 = types.KeyboardButton('网易云热评')
button10 = types.KeyboardButton('蓝奏云解析')
button11 = types.KeyboardButton('一言堂')
button12 = types.KeyboardButton('关闭键盘')

keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11, button12)

# /start 命令处理函数
@bot.message_handler(commands=['start'])
def handle_start(message):
    welcome_message = (
        "欢迎使用工具盒子机器人!🎈\n\n"
        "发送 /start 开始程序\n"
        "发送 /menu 开启键盘\n"
        "发送 /close 关闭键盘\n"
        "发送 /help 获取命令"
    )
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def handle_help(message):
    help_message = (
        "/start - 开始程序\n"
        "/menu - 开启键盘\n"
        "/close - 关闭键盘\n"
        "/help - 获取命令"
    )
    bot.send_message(message.chat.id, help_message, reply_markup=keyboard)

# 文本消息处理函数
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == '/menu':
        bot.send_message(message.chat.id, "已开启键盘", reply_markup=keyboard)
    elif message.text == '关闭键盘' or message.text == '/close':
        bot.send_message(message.chat.id, "已关闭键盘", reply_markup=types.ReplyKeyboardRemove())
    elif message.text == '文本转二维码':
        bot.send_message(message.chat.id, "请回复要转换成二维码的文本内容:")
        bot.register_next_step_handler(message, generate_qrcode)
    elif message.text == 'base64编码':
        bot.send_message(message.chat.id, "请回复要 Base64 编码的文本内容:")
        bot.register_next_step_handler(message, encode_base64)
    elif message.text == 'base64解码':
        bot.send_message(message.chat.id, "请回复要解码的 Base64 文本内容:")
        bot.register_next_step_handler(message, decode_base64)
    elif message.text == '随机密码生成':
        bot.send_message(message.chat.id, generate_random_password())
    elif message.text == 'uuid生成器':
        bot.send_message(message.chat.id, generate_uuid())
    elif message.text == '必应每日壁纸':
        download_bing_wallpaper(message.chat.id)
    elif message.text == '图片转ico图标':
        bot.send_message(message.chat.id, "请回复一个 jpg 或 png 图片文件:")
        bot.register_next_step_handler(message, convert_to_ico)
    elif message.text == '舔狗日记':
        send_request_data(message.chat.id, 'https://cloud.qqshabi.cn/api/tiangou/api.php')
    elif message.text == '网易云热评':
        send_request_data(message.chat.id, 'https://cloud.qqshabi.cn/api/comments/api.php?format=text')
    elif message.text == '一言堂':
        send_request_data(message.chat.id, 'https://cloud.qqshabi.cn/api/hitokoto/hitokoto.php')
    elif message.text == '蓝奏云解析':
        bot.send_message(message.chat.id, "请发送蓝奏云链接进行解析：")
        bot.register_next_step_handler(message, handle_lanzou_url)

# 蓝奏云解析处理函数
def handle_lanzou_url(message):
    user_url = message.text.strip()
    api_url = API_BASE_URL + user_url

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 200 and "data" in data:
            download_url = data["data"]
            bot.send_message(message.chat.id, f"解析成功！下载链接为：\n{download_url}")
        else:
            bot.send_message(message.chat.id, "解析失败，返回的内容中没有包含下载链接。")
    except requests.exceptions.RequestException as e:
        bot.send_message(message.chat.id, f"请求发生错误：{e}")

# 工具函数
def generate_qrcode(message):
    text = message.text
    img = qrcode.make(text)
    img.save('qrcode.png')
    with open('qrcode.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    os.remove('qrcode.png')

def encode_base64(message):
    text_bytes = message.text.encode('utf-8')
    base64_text = base64.b64encode(text_bytes).decode('ascii')
    bot.send_message(message.chat.id, base64_text)

def decode_base64(message):
    try:
        decoded_text = base64.b64decode(message.text).decode('utf-8')
        bot.send_message(message.chat.id, decoded_text)
    except Exception:
        bot.send_message(message.chat.id, "解码失败，请确认输入内容是否为有效的 Base64 编码。")

def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(12))

def generate_uuid():
    return str(uuid.uuid4())

def download_bing_wallpaper(chat_id):
    url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US'
    try:
        response = requests.get(url)
        wallpaper_path = response.json()['images'][0]['url']
        wallpaper_url = 'https://www.bing.com' + wallpaper_path
        wallpaper_response = requests.get(wallpaper_url)

        with open('bing_wallpaper.jpg', 'wb') as f:
            f.write(wallpaper_response.content)

        with open('bing_wallpaper.jpg', 'rb') as photo:
            bot.send_photo(chat_id, photo)
        os.remove('bing_wallpaper.jpg')
    except Exception as e:
        bot.send_message(chat_id, "下载壁纸时发生错误。")

def convert_to_ico(message):
    try:
        if message.content_type == 'photo':
            file_info = bot.get_file(message.photo[-1].file_id)
            file = requests.get(f'https://api.telegram.org/file/bot{API_KEY}/{file_info.file_path}')
            with open('temp_image.png', 'wb') as f:
                f.write(file.content)

            img = Image.open('temp_image.png')
            img.save('icon.ico', format='ICO')

            with open('icon.ico', 'rb') as f:
                bot.send_document(message.chat.id, f)
            os.remove('temp_image.png')
            os.remove('icon.ico')
        else:
            bot.send_message(message.chat.id, "请发送图片文件。")
    except Exception:
        bot.send_message(message.chat.id, "处理图片时发生错误。")

def send_request_data(chat_id, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bot.send_message(chat_id, response.text)
        else:
            bot.send_message(chat_id, "获取数据失败，请稍后再试。")
    except Exception:
        bot.send_message(chat_id, "请求发生错误。")

# 启动机器人
bot.polling()
