import telebot
from telebot import types

TOKEN = '7750324003:AAGn7mGaXTW9TG07xr4iCAGPCZGEVFWhkNA'
bot = telebot.TeleBot(TOKEN)

user_orders = {}

# Командаи /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("📷 Instagram")
    btn2 = types.KeyboardButton("🛒 Заказать")
    btn3 = types.KeyboardButton("ℹ️ О нас")
    btn4 = types.KeyboardButton("📞 Контакт")
    markup.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, "Салом! Хуш омадед ба EasyBot.TJ 👋", reply_markup=markup)

# Обработка кнопок меню
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "📷 Instagram":
        markup = types.InlineKeyboardMarkup()
        insta_btn = types.InlineKeyboardButton(
            text="👉 Перейти в Instagram",
            url="https://www.instagram.com/easybot.tj?igsh=cTIzem0xMG4yNTI0"
        )
        markup.add(insta_btn)
        bot.send_message(
            message.chat.id,
            "📸 Инстаграми мо дар зер:",
            reply_markup=markup
        )

    elif message.text == "🛒 Заказать":
        msg = bot.send_message(message.chat.id, "Лутфан, номи худро ворид кунед:")
        bot.register_next_step_handler(msg, process_name)

    elif message.text == "ℹ️ О нас":
        bot.send_message(
            message.chat.id,
            "📦 EasyBot — боти фармоиш ва дастгирӣ дар Тоҷикистон. Мо бо шумо 24/7!"
        )

    elif message.text == "📞 Контакт":
        bot.send_message(
            message.chat.id,
            "📞 Барои тамос бо мо:\n📱 +992 780 310 909\n✉️ Email: support@easybot.tj"
        )

# Гирифтани ном
def process_name(message):
    user_id = message.chat.id
    user_orders[user_id] = {'name': message.text}
    msg = bot.send_message(user_id, "Рақами телефони худро ворид кунед:")
    bot.register_next_step_handler(msg, process_phone)

# Гирифтани телефон ва сабт ба файл
def process_phone(message):
    user_id = message.chat.id
    phone = message.text
    name = user_orders[user_id]['name']

    with open("orders.txt", "a", encoding='utf-8') as f:
        f.write(f"Ном: {name}, Телефон: {phone}\n")

    bot.send_message(user_id, f"✅ Фармоиши шумо қабул шуд!\n\nНом: {name}\nТелефон: {phone}")

# Запуск бота
bot.polling(none_stop=True)
