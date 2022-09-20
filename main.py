import os
from get_stocks import ticker_engine
from scraping import scrape_engine
from check_pdufa_list import delete_duplicates, remove_passed_dates
from telegram_bot import telegram_bot_sendtext, telegram_send_image
from remove_passed_dates_ticker import remove_passed_dates_ticker_info
from ticker_update import update_ticker
import schedule
import time


def updating_ticker():
    remove_passed_dates_ticker_info()

    text, img = update_ticker()

    return text, img

def scrape_and_get_stock_info_engine():
    scrape_engine()

    delete_duplicates()

    remove_passed_dates()

    text, img = ticker_engine()

    return text, img


def remove_image():
    dir = 'ticker_images'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    return




def one_per_hour():
    text, filepath = scrape_and_get_stock_info_engine()
    time.sleep(1)
    i = 0


    while True:

        if len(text) == 0 or len(filepath) == 0:
            break

        elif i >= len(text):
            break
        else:
            tex_to_be_sent = text[i]
            image = filepath[i]
            message = 'New Message:\n' + tex_to_be_sent
            telegram_bot_sendtext(message)
            telegram_send_image(image)

            time.sleep(3)
        i += 1

    remove_image()

    return


def updating():

    text, filepath = updating_ticker()
    time.sleep(1)
    i = 0

    while True:

        if len(text) == 0 or len(filepath) == 0:
            break

        elif i >= len(text):
            break
        else:
            tex_to_be_sent = text[i]
            image = filepath[i]
            message = 'New Message:\n' + tex_to_be_sent
            telegram_bot_sendtext(message)
            telegram_send_image(image)

            time.sleep(3)
        i += 1

    return





schedule.every().hour.do(one_per_hour)
schedule.every(7).minutes.do(updating)

while True:
    schedule.run_pending()
    time.sleep(1)













