import telebot
import asyncio
import pickle
import os
from collections import defaultdict
from telebot import types  
from telebot.async_telebot import AsyncTeleBot 
TOKEN = '7760865310:AAFkg2rKtm0WlbZFwNQ9TywbO69VWzchNpQ'
Bot = AsyncTeleBot(TOKEN)
states = defaultdict(lambda: {"state":"start"})
def save():
    global states
    s = pickle.dumps(states)
    with open("state.pickle","wb") as file:
        file.write(s)
def load():
    global states
    if os.path.isfile("state.pickle"):
        s = ""
        with open("state.pickle", mode = "rb") as file:
            s = file.read()
        states = pickle.loads(s)
load()
@Bot.message_handler(commands= ["ava"])
async def send_avatar(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username
    photos = Bot.get_user_profile_photos(user_id)
    if photos.total_count > 0:
        photo = photos.photos [-1][-1]
        await Bot.send_photo(message.chat.id, photo.file_id, caption=f'Аватарка пользователя {first_name} (@{username})')
    else:
        await Bot.reply_to(message, "У вас нет аватарки.")
@Bot.message_handler(commands= ["start"])
async def start(message: types.Message):
    await Bot.reply_to(message, "Привет, для того что бы заказать пиццу напиши команду \"/pizza\"")
@Bot.message_handler(commands= ["pizza"])
async def pizza(message: types.Message):
    await Bot.reply_to(message, "Пожалуйста введите ваше имя")
    states[message.from_user.id]["state"] = "name"
@Bot.message_handler(commands= ["info"])
async def info(message: types.Message):
    await Bot.reply_to(message, states[message.from_user.id]["state"])
    await Bot.reply_to(message, f"{states[message.from_user.id]["name"]}\n{states[message.from_user.id]["address"]}\n{states[message.from_user.id]["pizza"]}")
@Bot.message_handler(commands= ["image"])
async def imagee(message: types.Message):
    file_path = r"C:\Users\Asus\Desktop\Bot_Tg\i (23).webp"
    file = open(file_path, "rb")
    await Bot.send_photo(message.chat.id, file, "Смешарики")
    file.close()
@Bot.message_handler(content_types= ["photo"])
async def image_from_user(message: types.Message):
    file_info = Bot.get_file(message.photo[-1].file_id)
    download = Bot.download_file(file_info.file_path)
    format = file_info.file_path.split(".")[-1]
    file = open(f"image.{format}", "wb")
    file.write(download)
    file.close()
    await Bot.reply_to(message, "Изображение загружено")
@Bot.message_handler(content_types= ["text"])
async def echo(message: types.Message):
    state = states[message.from_user.id]["state"]
    if state == "name":
        states[message.from_user.id]["name"] = message.text
        await Bot.reply_to(message, "Введите ваш адрес")
        states[message.from_user.id]["state"] = "address"
    if state == "address":
        states[message.from_user.id]["address"] = message.text
        await Bot.reply_to(message, "Укажите название пиццы")
        states[message.from_user.id]["state"] = "pizza"
    if state == "pizza":
        pizza = message.text 
        id = message.from_user.id
        if id not in states:
            states[id] = {}
        states[id]["pizza"] = pizza
        save()
        await Bot.reply_to(message,"Ваша пицца в пути")
        info(message)
        states[message.from_user.id]["state"] = "start"


asyncio.run(Bot.infinity_polling())


