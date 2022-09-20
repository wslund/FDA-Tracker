# FDA-Calender

This is a script that retrieves which companies have submitted an application to get a drug approved by the FDA. The program then retrieves information about the company's stock price and sends that information out on a Telegram channel:
- price
- resistance
- support
The script then keeps track of how the share price is going. If the stock price breaks above resistance or breaks below support, a new message is sent to the telegram channel.

To run the script:
1. create a bot on telegram,
2. enter your Token and Id on telegram_bot.py
3. Then run main.py (you can change the timer to the time you want).
