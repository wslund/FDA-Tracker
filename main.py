import schedule
import time
import asyncio
import os
import discord
from get_stocks import ticker_engine
from scraping import scrape_engine
from check_pdufa_list import delete_duplicates, remove_passed_dates
from KEY import TOKEN

















''''
def test_timer():
    print("is in test timer")
    #scrape_engine()
    #delete_duplicates()
    remove_passed_dates()
    return



schedule.every(1).minutes.do(test_timer)

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(1)

'''























client = discord.Client()








async def engine_ticker():
    scrape_engine()
    delete_duplicates()
    remove_passed_dates()
    text, img = ticker_engine()
    return text, img

async def remove_image(filepath):
    os.remove(filepath)
    return


async def one_per_hour():

    task = asyncio.create_task(engine_ticker())
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
                channel = client.get_channel(1001169548961132566)
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











