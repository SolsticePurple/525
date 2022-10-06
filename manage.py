import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import os 

class User:
    def __init__(self, uid):
        self.uid = uid
        self.cart = []  # tuples (eid, amount)
        self.state = "drochit"

    #functions add_to_cart, set_state


main_keyboard = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Предложения сегодняшнего ня"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Инфо"
            },
            "color": "positive"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"3\"}",
                    "label": "Заказ"
                },
                "color": "positive"
        }
        ],

    ]
}


zaloop_keyboard = {
    "one_time": False,
    "inline": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "Предложения сегодняшнего ня"
            },
            "color": "positive"
        }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Инфо"
            },
            "color": "positive"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"3\"}",
                    "label": "Заказ"
                },
                "color": "positive"
        }
        ],

    ]
}

admin_buttons = ("Добавить", "Удалить", "Что есть?")


def col(i):
    return ("positive", "negative", "secondary")[i]


admin_main_keyboard = {
    "one_time": False,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"" + str(c) + "\"}",
                    "label": i
                },
                "color": col(c)
            } for c, i in enumerate(admin_buttons)
        ]
    ]
}


def print_stuff(stuff):
    if len(stuff) == 0:
        return "ВЫ ОБАНКРОТИЛИСЬ"
    return "\n--------------------------\n".join([f"{c + 1})Название: {i['name']}\nЦена: {i['price']}\n Кол-во: {i['amount']}" for c, i in enumerate(stuff)])


def item2btn(i):
    return [
        {
            "action": {
                "type": "text",
                "payload": "{}",
                "label": i["name"]
            },
            "color": "positive"
        }
    ]


def stuff_keyboard(stuff):
    return {
        "one_time": False,
        "inline": True,
        "buttons": list(map(item2btn, stuff))
    }


def write_msg(user_id, message, key="{}"):
    k = json.dumps(key, ensure_ascii=False).encode('utf-8')
    k = str(k.decode('utf-8'))
    vk.method('messages.send',
              {'user_id': user_id,
               'message': message,
               'keyboard': k,
               'random_id': random.randint(0, 2048)})


TOKEN = os.getenv("VK_BOT_TOKEN")

vk = vk_api.VkApi(token=TOKEN)
vkget = vk.get_api()
longpoll = VkLongPoll(vk)
attachment = 'photo-216333182_457239017'
users = []

stuff = [
    {
        "name": "Purple Genezis r34",
        "price": 123,
        "amount": 3
    },
    {
        "name": "zaloop",
        "price": 22,
        "amount": 2
    }
]
new_eng = {}

admin_ids = []  # [237849534, 414987644]
admin_eng_state = ""  # "WAIT_NAME", "WAIT_PRICE", "WAIT_AMOUNT", "WAIT_REMOVE_ID"

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            if event.user_id in admin_ids:
                if admin_eng_state == "" and event.text not in admin_buttons:
                    write_msg(event.user_id, "Вы админ\nИДИТЕ НАХУЙ",
                              admin_main_keyboard)
                elif admin_eng_state == "" and event.text == "Добавить":
                    admin_eng_state = "WAIT_NAME"
                    write_msg(event.user_id, "Название")
                elif admin_eng_state == "" and event.text == "Удалить":
                    write_msg(
                        event.user_id, f"Выбери номер для удаления \n{print_stuff(stuff)}")
                    admin_eng_state = "WAIT_REMOVE_ID"
                elif admin_eng_state == "" and event.text == "Что есть?":
                    write_msg(event.user_id, print_stuff(stuff))
                elif admin_eng_state == "WAIT_NAME":
                    new_eng["name"] = event.text
                    admin_eng_state = "WAIT_PRICE"
                    write_msg(event.user_id, "Цена")

                elif admin_eng_state == "WAIT_PRICE":
                    try:
                        i = int(event.text)
                        new_eng["price"] = i
                        admin_eng_state = "WAIT_AMOUNT"
                        write_msg(event.user_id, "Количество")
                    except ValueError:
                        write_msg(event.user_id, "Ты проебался")

                elif admin_eng_state == "WAIT_AMOUNT":
                    try:
                        i = int(event.text)
                        new_eng["amount"] = i
                        admin_eng_state = ""
                        stuff.append(dict(new_eng))
                        write_msg(event.user_id, "Готово")
                    except ValueError:
                        write_msg(event.user_id, "Ты проебался")

                elif admin_eng_state == "WAIT_REMOVE_ID":
                    try:
                        i = int(event.text)
                        del stuff[i - 1]
                        admin_eng_state = ""
                        write_msg(event.user_id, "УДОЛЕНО")
                    except:
                        write_msg(event.user_id, "Ты проебался")
            else:
                #user = next()#try to find user if not exist create new
                if event.text.lower() == "предложения сегодняшнего ня":
                    vk.method('messages.send', {
                              'user_id': event.user_id, 'message': "Solar power\n 70 рублей 1шт \n 65 руб от 2шт ", "attachment": attachment, 'random_id': (0)})
                if event.text == "Заказ":
                    write_msg(event.user_id, print_stuff(
                        stuff), stuff_keyboard(stuff))
                else:
                    write_msg(
                        event.user_id, "Кто вы такие\nя вас не звал\nИДИТЕ НАХУЙ", main_keyboard)
