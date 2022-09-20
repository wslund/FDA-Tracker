import time
import schedule
import requests
from KEY import Telegram_Token, bot_chatID



def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + Telegram_Token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

def telegram_send_image(file_path):
    files = {'photo': open(file_path, 'rb')}
    resp = requests.post('https://api.telegram.org/bot' + Telegram_Token + '/sendPhoto?chat_id=' + bot_chatID, files=files)
    return resp








