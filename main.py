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
# bot = telebot.TeleBot('6058236364:AAHlMLUhcETG6VdZhCg57PIzX7PcTjDe8NQ')

keyboard = types.ReplyKeyboardMarkup(row_width=3,resize_keyboard=True)
# 添加按钮到键盘
button1 = types.KeyboardButton('文本转二维码')
button2 = types.KeyboardButton('base64编码')
button3 = types.KeyboardButton('base64解码')
button4 = types.KeyboardButton('随机密码生成')
button5 = types.KeyboardButton('uuid生成器')
button6 = types.KeyboardButton('必应每日壁纸')
button7 = types.KeyboardButton('图片转ico图标')
button8 = types.KeyboardButton('舔狗日记')
button9 = types.KeyboardButton('关闭键盘')

keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)


# /start命令处理函数
@bot.message_handler(commands=['start'])
def handle_start(message):
    global keyboard_open
    keyboard_open = True
    welcome_message = "欢迎使用工具盒子机器人!🎈\n\n发送 /start 开始程序\n发送 /menu 开启键盘\n发送 /close 关闭键盘\n发送 /help 获取命令"
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def handle_start(message):
    global keyboard_open
    keyboard_open = True
    welcome_message = "start-开始程序\nmenu-开启键盘\nclose-关闭键盘\nhelp-获取命令"
    bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)

# 文本消息处理函数
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    global keyboard_open
    if message.text == '/menu':
        keyboard_open = True
        bot.send_message(message.chat.id, "已开启键盘", reply_markup=keyboard)
    elif message.text == '关闭键盘':
        keyboard_open = False
        bot.send_message(message.chat.id, "已关闭键盘", reply_markup=types.ReplyKeyboardRemove())
    if message.text == '/close':
        keyboard_open = False
        bot.send_message(message.chat.id, "已关闭键盘", reply_markup=types.ReplyKeyboardRemove())
    if message.text == '文本转二维码':
        bot.send_message(message.chat.id, "请回复要转换成二维码的文本内容:")
        bot.register_next_step_handler(message, generate_qrcode)
    elif message.text == 'base64编码':
        bot.send_message(message.chat.id, "请回复要Base64编码的文本内容:")
        bot.register_next_step_handler(message, encode_base64)
    elif message.text == 'base64解码':
        bot.send_message(message.chat.id, "请回复要解码的Base64文本内容:")
        bot.register_next_step_handler(message, decode_base64)
    elif message.text == '随机密码生成':
        bot.send_message(message.chat.id, generate_random_password())
    elif message.text == 'uuid生成器':
        bot.send_message(message.chat.id, generate_uuid())
    elif message.text == '必应每日壁纸':
        download_bing_wallpaper(message.chat.id)
    elif message.text == '图片转ico图标':
        bot.send_message(message.chat.id, "请回复一个jpg或png图片文件:")
        bot.register_next_step_handler(message, convert_to_ico)
    elif message.text == '舔狗日记':
        response = requests.get('https://cloud.qqshabi.cn/api/tiangou/api.php')
        if response.status_code == 200:
            diary = response.text
            bot.send_message(message.chat.id, diary)
        else:
            bot.send_message(message.chat.id, '获取舔狗日记失败，请稍后再试。')


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


# 图片转ico
def convert_to_ico(message):
    # 检查用户回复的消息是否包含图片
    if message.content_type != 'photo':
        bot.send_message(message.chat.id, "请回复一个jpg或png图片文件。")
        return

    # 获取用户回复的图片
    API_KEY = "6058236364:AAHlMLUhcETG6VdZhCg57PIzX7PcTjDe8NQ"
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    file = requests.get('https://api.telegram.org/file/bot{}/{}'.format(API_KEY, file_info.file_path))

    # 将图片保存到本地
    image_path = 'image.jpg'  # 保存图片的文件名，可以根据需要进行修改
    with open(image_path, 'wb') as f:
        f.write(file.content)

    # 转换图片为ico格式
    try:
        image = Image.open(image_path)
        if image.format not in ['JPEG', 'PNG']:
            bot.send_message(message.chat.id, "只支持jpg和png格式的图片。")
            return

        ico_path = 'icon.ico'  # 保存ico图标的文件名，可以根据需要进行修改
        image.save(ico_path, format='ICO')

        # 发送ico图标给用户
        with open(ico_path, 'rb') as f:
            bot.send_document(message.chat.id, f)

        # 删除临时文件
        os.remove(image_path)
        os.remove(ico_path)
    except Exception as e:
        bot.send_message(message.chat.id, "转换图片时发生错误。")



bot.polling()
