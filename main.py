import asyncio
import schedule
import time
import os
import discord
from scrape_and_get_company.get_stocks import ticker_engine
from scrape_and_get_company.scraping import scrape_engine
from scrape_and_get_company.check_pdufa_list import delete_duplicates, remove_passed_dates
from KEY import TOKEN, CHANNEL
from update_ticker.remove_passed_dates_ticker import remove_passed_dates_ticker_info
from update_ticker.ticker_update import update_ticker


client = discord.Client()


async def updating_ticker():
    remove_passed_dates_ticker_info()
    text, img = update_ticker()
    return text, img

async def scrape_and_get_stock_info():
    scrape_engine()
    delete_duplicates()
    remove_passed_dates()
    text, img = ticker_engine()
    return text, img

async def remove_image(filepath):
    os.remove(filepath)
    return


async def one_per_hour():

    task = asyncio.create_task(scrape_and_get_stock_info())
    check = await task

    text, img = check

    i = 0
    while True:

        if len(text) == 0 or len(img) == 0:
            break

        elif i >= len(text):
            break
        else:
            tex_to_be_sent = text[i]
            image = img[i]

            with open(image, "rb") as fh:
                channel = client.get_channel(CHANNEL)
                file = discord.File(fh, filename=image)
                message = f'New Message:\n{tex_to_be_sent}'

                await channel.send(message)
                await channel.send(file=file)

        await remove_image(image)
        i += 1

    return

async def one_per_seventeen_minute():

    task = asyncio.create_task(updating_ticker())
    check = await task

    text, img = check

    i = 0
    while True:

        if len(text) == 0 or len(img) == 0:
            break

        elif i >= len(text):
            break
        else:
            tex_to_be_sent = text[i]
            image = img[i]

            with open(image, "rb") as fh:
                channel = client.get_channel(CHANNEL)
                file = discord.File(fh, filename=image)
                message = f'New Message:\n{tex_to_be_sent}'

                await channel.send(message)
                await channel.send(file=file)

        await remove_image(image)
        i += 1

    return


@client.event
async def on_ready():
    await one_per_hour()





client.run(TOKEN)
asyncio.run(one_per_hour())



schedule.every().hour.do(one_per_hour())


while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)









