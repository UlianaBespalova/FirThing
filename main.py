import time

import requests
import telebot
import urllib3

delay = 60
data_url = 'https://raw.githubusercontent.com/UlianaBespalova/FirThing/main/data.txt'
bot = telebot.TeleBot('5278194362:AAG1EsKjB9bEQrAryFx6EqOlN0b-2OtZ7a8')
id = 631275114


def get_data_by_url(url):
    f = requests.get(url)
    res = []
    for string in f.text.split('\n')[:-1]:
        res.append(string.split('|'))
    return res


# def get_data_from_file(filename):
#     f = open(filename, 'r', encoding='UTF-8')
#     str_list = f.read().split('\n')[:-1]
#     f.close()
#     res = []
#     for string in str_list:
#         res.append(string.split('|'))
#     return res


# ------------------------------------------------------
WB_discount = 1
WB_flower_string = "🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸🌸\n"
WB_error_string = "🌸🍎🌸🍎🌸🍎🌸🍎🌸🍎🌸🍎🌸🍎🌸🍎🌸\n"


def WB_create_Alarm_message(res):
    string = WB_flower_string + "\nALARM\n\n"
    for item in res:
        new_str = item[0] + " : " + str(item[3]) + "\n" + item[1] + "\n"
        string += new_str
    string += "\n" + WB_flower_string
    return string


def WB_create_Error_message(errors):
    string = WB_error_string + "\nWB ERROR\nНе удалось выкопать данные\n\n"
    # for error in errors:
    #     new_str = error[0] + " - " + error[1] + "\n"
    #     string += new_str
    string += "\n" + WB_error_string
    return string


def WB_monitoring_get_price(wb_url):
    http = urllib3.PoolManager()
    resp = http.request('GET', wb_url)
    resp_html = resp.data.decode('utf-8')
    price = 0
    try:
        price = resp_html.split('"salePrice":')[1].split(',"priceDetails"')[0]
    except:
        pass
    if price is not None:
        try:
            price = int(price) * (1 - WB_discount * 0.01)
        except:
            price = price.split('}')[0]
            price = int(price) * (1 - WB_discount * 0.01)
        return price
    else:
        return 0


def WB_monitoring_check_item(item):
    price = WB_monitoring_get_price(item[1])
    # print("-----------", price)
    print(item[0], price)
    if price == 0:
        return 'error'
    if price <= int(item[2]):
        item.append(int(price))
        return item


def WB_monitoring_check_data():
    # wb_urls_list = get_data_from_file('data.txt')
    wb_urls_list = get_data_by_url(data_url)

    res = []
    error = False
    for item in wb_urls_list:
        res_item = WB_monitoring_check_item(item)
        if res_item == 'error':
            res.append(item)
            error = True
        elif res_item is not None:
            res.append(res_item)
    return res, error


def WB_monitoring_get_res_message():
    res, error = WB_monitoring_check_data()
    if len(res) == 0:
        return "🍀 I'm alive, but nothing happens 🍀"
        # return None
    if error:
        return WB_create_Error_message(res)
    else:
        return WB_create_Alarm_message(res)


def WB_monitoring():
    message = WB_monitoring_get_res_message()
    if message is not None:
        bot.send_message(id, message)
    time.sleep(delay)


# ------------------------------------------------------


# @bot.message_handler(commands=["start"])
# def start(m, res=False):
#     bot.send_message(m.chat.id, 'Hi')


# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     bot.send_message(message.chat.id, 'bip')

# bot.polling(none_stop=True, interval=0)

while True:
    # bot.send_message(id, 'bip')
    WB_monitoring()

# if __name__ == '__main__':
#     ivan('PyCharm')
