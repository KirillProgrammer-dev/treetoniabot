from codecs import replace_errors
from csv import excel
import telebot
from telebot import types
from Order import Order
from Excel import Excel 
import time
import datetime
from threading import Thread

bot = telebot.TeleBot("5203991048:AAHAy43v41b5jumeqczpr559jv3VfXOVsXw")

with open("start.txt", encoding="utf-8") as f:
    start = f.read()

#ADMIN FUNCTIONS

admin_id = [244162514, 1470689869]

@bot.message_handler(commands=['all'])
def all(message):
    if message.from_user.id in admin_id:
        file = open("./orders.xlsx", "rb")
        bot.send_document(message.from_user.id, file)

@bot.message_handler(commands=['delete'])
def delete(message):
    if message.from_user.id in admin_id:
        bot.send_message(message.from_user.id, "Пришлите id пользователя, пожалуйста")
        bot.register_next_step_handler(message, delete_id)

def delete_id(message):
    excel = Excel()
    excel.delete(message.text)
    bot.send_message(message.from_user.id, "Удаление прошло успешно")

@bot.message_handler(commands=['settimes'])
def settime(message):
    if message.from_user.id in admin_id:
        bot.send_message(message.from_user.id, "Пришлите, пожалуйста, удобные даты для отдачи саженцев через запятую(предыдущие даты удалятся)")
        bot.register_next_step_handler(message, get_time_admin)

def get_time_admin(message):
    all_dates = str(message.text)
    with open("dates.txt", "w", encoding="utf-8") as f:
        f.write(all_dates)
    bot.send_message(message.from_user.id, "Даты уставлены успешно")

#END

#ORDER FUNCTIONS

def create_order(message):
    global creating_order
    creating_order = True
    excel = Excel()
    if not excel.check_spam(message.from_user.id):
        global order
        order = Order()
        bot.send_message(message.from_user.id, "Введите Ваш адрес электронной почты")
        bot.register_next_step_handler(message, get_email)
    else:
        bot.send_message(message.from_user.id, "Вы уже сделали 1 заказ, если хотите изменить его напишите /editorder")


@bot.message_handler(commands=['editorder'])
def edit_order(message):
        bot.send_message(message.from_user.id, """Если вы хотите изменить почту введите /editemail
Если вы хотите изменить ФИО введите /editfio
Если вы хотите изменить телефон введите /editphone
Если вы хотите изменить количество саженцев введите /editamount
Если вы хотите изменить место введите /editplace
Если вы хотите изменить дату введите /editdate
Если вы хотите изменить комментарий введите /editcomment
        """)

@bot.message_handler(commands=['editemail'])
def edit_email(message):
    bot.send_message(message.from_user.id, 'Введите новую почту')
    bot.register_next_step_handler(message, get_email_new)

def get_email_new(message):
    excel = Excel()
    order = Order()
    if excel.check_spam(message.from_user.id):
        if order.validate_email(message.text):
            excel.edit(message.from_user.id, "B", message.text)
            bot.send_message(message.from_user.id, 'Почта удачно обновилась, новая почта -' + message.text)
        else:
            bot.send_message(message.from_user.id, 'Такой почты не существует')
            edit_email(message)
    else:
        bot.send_message(message.from_user.id, "Вы не оставляли заказ у нас")

@bot.message_handler(commands=['editfio'])
def edit_fio(message):
    bot.send_message(message.from_user.id, 'Введите новое ФИО')
    bot.register_next_step_handler(message, get_fio_new)

def get_fio_new(message):
    excel = Excel()
    if excel.check_spam(message.from_user.id):
        excel.edit(message.from_user.id, "C", message.text)
        bot.send_message(message.from_user.id, 'ФИО удачно обновилось, новое ФИО -' + message.text)
    else:
        bot.send_message(message.from_user.id, "Вы не оставляли заказ у нас")

@bot.message_handler(commands=['editphone'])
def edit_phone(message):
    bot.send_message(message.from_user.id, 'Введите новый телефон')
    bot.register_next_step_handler(message, get_phone_new)

def get_phone_new(message):
    excel = Excel()
    order = Order()
    if excel.check_spam(message.from_user.id):
        if order.validate_phone(message.text):
            excel.edit(message.from_user.id, "D", message.text)
            bot.send_message(message.from_user.id, 'Телефон удачно обновился, новый телефон -' + message.text)
        else:
            bot.send_message(message.from_user.id, "Телефон не существует или зарегестрирован не в Российской зоне")
            edit_phone(message)
    else:
        bot.send_message(message.from_user.id, "Вы не оставляли заказ у нас")

@bot.message_handler(commands=['editamount'])
def edit_amount(message):
    bot.send_message(message.from_user.id, 'Введите новое количество')
    bot.register_next_step_handler(message, get_amount_new)

def get_amount_new(message):
    excel = Excel()
    if excel.check_spam(message.from_user.id):
        excel.edit(message.from_user.id, "E", message.text)
        bot.send_message(message.from_user.id, 'Коллчество удачно обновилось, новое количество -' + message.text)
    else:
        bot.send_message(message.from_user.id, "Вы не оставляли заказ у нас")

@bot.message_handler(commands=['editplace'])
def edit_place(message):
    bot.send_message(message.from_user.id, 'Введите новое место')
    bot.register_next_step_handler(message, get_place_new)

def get_place_new(message):
    excel = Excel()
    if excel.check_spam(message.from_user.id):
        excel.edit(message.from_user.id, "F", message.text)
        bot.send_message(message.from_user.id, 'Место удачно обновилось, новое место -' + message.text)
    else:
        bot.send_message(message.from_user.id, "Вы не оставляли заказ у нас")

@bot.message_handler(commands=['editdate'])
def edit_date(message):
    markup_inline = types.InlineKeyboardMarkup()
    with open("dates.txt", "r", encoding="utf-8") as f:
        all_dates = f.read().split(",")
    for i in all_dates:
        markup_inline.add(types.InlineKeyboardButton(text=i, callback_data=str("editdate" + str(i))))

    bot.send_message(message.from_user.id, 'Укажите удобную дату получения', reply_markup=markup_inline)
    

@bot.message_handler(commands=['editcomment'])
def edit_comment(message):
    bot.send_message(message.from_user.id, 'Введите новый комментарий')
    bot.register_next_step_handler(message, get_comment_new)

def get_comment_new(message):
    excel = Excel()
    if excel.check_spam(message.from_user.id):
        excel.edit(message.from_user.id, "H", message.text)
        bot.send_message(message.from_user.id, 'Комментарий удачно обновился, новый комментарий -' + message.text)
    else:
        bot.send_message(message.from_user.id, "Вы не оставляли заказ у нас")

@bot.message_handler(commands=['showorder'])
def show_order(message):
    excel = Excel()
    all = excel.show_order(message.from_user.id)
    bot.send_message(message.from_user.id, all)

#END

#MAIN FUNCTION
creating_order = False
@bot.message_handler(commands=['help'])
def help(message):
    markup = types.InlineKeyboardMarkup()
    chat = types.InlineKeyboardButton("Наш телеграмм чат", url="https://t.me/joinchat/aTpIbg3esacyMTY6")
    markup.add(chat)
    bot.send_message(message.from_user.id, "По всем вопросам пишите сюда", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, start)

    elif message.text == "/neworder":
        create_order(message)

#END

#FUNCTIONS FOR CREATING ORDER

def get_email(message):
    global email
    email = message.text
    if order.validate_email(email):
        order.email = email
        bot.send_message(message.from_user.id, 'Напишите, пожалуйста, Ваше ФИО')
        bot.register_next_step_handler(message, get_fio)
    else:
        bot.send_message(message.from_user.id, 'Такой почты не существует')
        create_order(message)

def get_fio(message, validate = False):
    if not validate:
        global fio
        fio = message.text
        order.name = fio
    if message.contact is not None:
        order.phone = message.contact 
    else:
        bot.send_message(message.from_user.id, 'Укажите телефон')
        bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    global phone
    phone = message.text
    order.phone = phone
    if order.validate_phone(message.text):
        bot.send_message(message.from_user.id, 'Укажите кол-во саженцев')
        bot.register_next_step_handler(message, get_amount)
    else:
        bot.send_message(message.from_user.id, "Телефон не существует или зарегестрирован не в Российской зоне")
        get_fio(message, True)

def get_amount(message):
    global amount
    amount = message.text
    order.amount = amount
    
    bot.send_message(message.from_user.id, 'Укажите место высадки')
    bot.register_next_step_handler(message, get_place)

def get_place(message):
    global place
    place = message.text
    order.place = place

    bot.send_message(message.from_user.id, 'Укажите комментарии к заказу')
    bot.register_next_step_handler(message, get_comments)


def get_comments(message):
    global comment
    comment = message.text
    order.comment = comment

    markup_inline = types.InlineKeyboardMarkup()
    with open("dates.txt", "r", encoding="utf-8") as f:
        all_dates = f.read().split(",")
    for i in all_dates:
        markup_inline.add(types.InlineKeyboardButton(text=i, callback_data=i))
        
    bot.send_message(message.from_user.id, 'Укажите удобную дату получения', reply_markup=markup_inline)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.find("editdate") != -1:
        excel = Excel()
        if excel.check_spam(call.from_user.id):
            excel.edit(call.from_user.id, "G", call.data.replace("editdate", ""))
            bot.send_message(call.from_user.id, 'Дата удачно обновилась, новая дата -' + call.data.replace("editdate", ""))
        else:
            bot.send_message(call.from_user.id, "Вы не оставляли заказ у нас")
    if creating_order:
        global date_giving
        date_giving = call.data
        order.date_giving = date_giving
        info = order.return_info(call.from_user.id)
        print(info)
        excel = Excel()
        excel.do_excel(info)
        bot.send_message(call.from_user.id, 'Заказ успешно создан')
    

#END

#MAIN CYCLE
class Thread1(Thread):
    def run(self): 
        while True:
            try:
                bot.polling(none_stop=True)
            except Exception as e:
                time.sleep(3)
                print(e)

class Thread2(Thread):
    def run(self):
        while True:
            with open("dates.txt", "r", encoding="utf-8") as f:
                all_dates = f.read().split(",")
                now = datetime.datetime.now()
                for i in all_dates:
                    try:
                        if datetime.datetime.strptime(i, '%d.%m') == datetime.datetime.strptime(f"{datetime.datetime.now().day}.{datetime.datetime.now().month}", "%d.%m"):
                            if int(now.time().hour) >= 10:
                                all_dates.remove(i)
                    except:
                        pass
                with open("dates.txt", "w", encoding="utf-8") as f:
                    #print(all_dates)
                    f.write(",".join(all_dates))

th2 = Thread2()
th2.start()
th1 = Thread1()
th1.start()


#END
