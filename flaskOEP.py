from flask import Flask, request
import telepot
import urllib3
import json
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

proxy_url = "http://proxy.server:3128"
telepot.api._pools = {
    'default': urllib3.ProxyManager(proxy_url=proxy_url, num_pools=3, maxsize=10, retries=False, timeout=30),
}
telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url=proxy_url, num_pools=1, maxsize=1, retries=False, timeout=30))

secret = "xxx"
bot = telepot.Bot('xxx')
bot.setWebhook("https://xxx.com/{}".format(secret), max_connections=1)
with open('data.json') as json_data:
    data = json.load(json_data)
    json_data.close()

app = Flask(__name__)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():

    update = request.get_json()
    if "callback_query" in update:
        flag=0
        query_id = update["callback_query"]["id"]
        chat_id = update["callback_query"]["message"]["chat"]["id"]
        text= update["callback_query"]["data"]
        keyboard = []
        if(text == 'type1'):
            for i in range(9):
                num = 'answer1 ' + str(i)
                keyboard.append([InlineKeyboardButton(text=data['question1'][i], callback_data=num)])

        elif(text == 'type2'):
            for i in range(7):
                num = 'answer2 ' +str(i)
                keyboard.append([InlineKeyboardButton(text=data['question2'][i], callback_data=num)])
        elif(text =='type3'):
            for i in range(4):
                num = 'answer3 ' +str(i)
                keyboard.append([InlineKeyboardButton(text=data['question3'][i], callback_data=num)])
        else:
            flag=1
            arr = str.split(text)
            answer = arr[0]
            number = arr[1]
            if(answer == 'answer1'):
                for i in range(9):
                    if(i==int(number)):
                        text = data['answer1'][int(number)]

            elif(answer == 'answer2'):
                for i in range(7):
                    if(i==int(number)):
                        text = data['answer2'][int(number)]

            elif(answer == 'answer3'):
                for i in range(4):
                    if(i==int(number)):
                        text = data['answer3'][int(number)]

        bot.answerCallbackQuery(query_id)
        if(flag==0):
            keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard)
            text= 'Please choose'
            bot.sendMessage(chat_id, text,reply_markup=keyboard)
        elif(flag==1):
            bot.sendMessage(chat_id, text)


    elif "message" in update:
        text = "Please select what you want to find out more about"
        chat_id = update["message"]["chat"]["id"]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Application', callback_data='type1')],
        [InlineKeyboardButton(text='Interview and Selection', callback_data='type2')],[InlineKeyboardButton(text='About the Program', callback_data='type3')]])
        bot.sendMessage(chat_id, text, reply_markup=keyboard)

    return "OK"