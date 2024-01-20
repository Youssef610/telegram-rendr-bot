import telebot
import requests
import time
import os
from keep_alive import keep_alive
keep_alive()
bot_token = '6673789871:AAGf-6reiWsjEHgYtXjlW0SDoh-8pKeaWJw'
bot = telebot.TeleBot(bot_token)

# Dictionary to store the processing status for each user ID
processing_status = {}

def find_valid_id(base_number, code,start):
    for i in range(start,100000):  # Iterate from 00000 to 99999
        usfnumber = str(i).zfill(5)
        generated_value = base_number + usfnumber
        response = requests.get(f"https://zaguni.vercel.app/get_stud_info?national_id={generated_value}").text
        if 'data' in response and code in response:
            
            return generated_value
        else:
            print(f'Fail: {generated_value}')

        if i % 10 == 0:
            os.system('clear')
            time.sleep(5)
            

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    processing_status[user_id] = False  # Initialize processing status for the user
    bot.send_message(message.chat.id, '''
        اهلا بيك فـ Usf Bot 
        ابعت الرقم الي عايز تبعتلو Spam بدون اي مسافات و عدد الرسايل علي الشكل ده👇
        010xxxxxxxx:عدد الرسايل 
    ''')

def isMsg(message):
    return True

@bot.message_handler(func=isMsg)
def reply(message):
    global processing_status
    try:
        Text = "حصل مشكله جرب تاني"
        user_id = message.from_user.username
        if user_id in processing_status and processing_status[user_id]:
            bot.reply_to(message, '''استني لما نخلص عشان نقدر نبعتلك  تاني 
مش كلو ورا بعضو كده 😏''')
            return

        bot.reply_to(message, "wait...")

        x = message.text
        if " " in x:
            x = x.replace(" ", "")
        if x[0] == "+":
            x = x[2:] 
        number = x[0:9]
        code = x[10:24]
        start=int(x[25:])
        print(number)
        print(code)
        print(start)

        processing_status[user_id] = True  # Set processing status to True for the current user
        try:
            Text = f"*ID is : * `{find_valid_id(number, code,start)}`"
            if not Text:
                Text = "No valid ID found"
        except:
            Text = "دخلت داتا غلط"

        bot.reply_to(message, Text,parse_mode='MarkdownV2')
        processing_status[user_id] = False  # Reset processing status for the current user
        bot.send_message(1098317745, f"{message.text}\nFrom: @{message.from_user.username}\nResponse: {Text}",parse_mode='MarkdownV2')

    except Exception as e:
        Text = "Faild"
        bot.reply_to(message, Text)
        print(e)

bot.polling()
