from email import message
from logging import exception
from xml.etree.ElementInclude import include
import telebot
import requests
import datetime
from bs4 import BeautifulSoup



bot = telebot.TeleBot("5259718399:AAHiGRdQ2O_OpQoCz4QFAqOqUH3wVGbY2RQ")


@bot.message_handler(commands=['nsbg'])
def redvoznje_nsbg(message):

    datum = datetime.datetime.now().date().strftime("%d.%m.%Y")
    vreme = datetime.datetime.now().time().strftime("%H:%M")

    url_ns_bg = "https://w3.srbvoz.rs/redvoznje//direktni/NOVI%20SAD/16808/BEOGRAD%20CENTAR/16052/"+datum+"/0000/sr"

    page_ns_bg = requests.get(url_ns_bg).text
    soup = BeautifulSoup(page_ns_bg, 'lxml')
    match_ns_bg = soup.find_all('b',text=True)
    del match_ns_bg[0:2]

    for i in range(0,len(match_ns_bg),4):
        match_ns_bg[i] = 0
        match_ns_bg[i+1] = 0

    match_ns_bg = list(filter((0).__ne__, match_ns_bg))

    for i in range(0,len(match_ns_bg)):
        match_ns_bg[i] = str(match_ns_bg[i])
        match_ns_bg[i] = match_ns_bg[i].strip('</b>')

    voz_ns_bg = {"polazak": [], "dolazak": []}

    for i in range(0,len(match_ns_bg),2):
        voz_ns_bg["polazak"].append(match_ns_bg[i])
        voz_ns_bg["dolazak"].append(match_ns_bg[i+1])

    reply_ns_bg = str()

    for i in range(0,len(voz_ns_bg["dolazak"])):
        reply_ns_bg += "Полазак: " + voz_ns_bg["polazak"][i] + '\n' + "Долазак: " + voz_ns_bg["dolazak"][i] + '\n\n'

    bot.reply_to(message,reply_ns_bg)

@bot.message_handler(commands=['bgns'])
def redvoznje_bgns(message):

    datum = datetime.datetime.now().date().strftime("%d.%m.%Y")
    vreme = datetime.datetime.now().time().strftime("%H:%M")

    url_bg_ns = "https://w3.srbvoz.rs/redvoznje//direktni/BEOGRAD%20CENTAR/16052/NOVI%20SAD/16808/"+datum+"/0000/sr"

    page_bg_ns = requests.get(url_bg_ns).text
    soup = BeautifulSoup(page_bg_ns, 'lxml')
    match_bg_ns = soup.find_all('b',text=True)
    del match_bg_ns[0:2]

    for i in range(0,len(match_bg_ns),4):
        match_bg_ns[i] = 0
        match_bg_ns[i+1] = 0

    match_bg_ns = list(filter((0).__ne__, match_bg_ns))

    for i in range(0,len(match_bg_ns)):
        match_bg_ns[i] = str(match_bg_ns[i])
        match_bg_ns[i] = match_bg_ns[i].strip('</b>')

    voz_bg_ns = {"polazak": [], "dolazak": []}

    for i in range(0,len(match_bg_ns),2):
        voz_bg_ns["polazak"].append(match_bg_ns[i])
        voz_bg_ns["dolazak"].append(match_bg_ns[i+1])

    reply_bg_ns = str()
    for i in range(0,len(voz_bg_ns["polazak"])):
        reply_bg_ns += "Полазак: " + voz_bg_ns["polazak"][i] + '\n' + "Долазак: " + voz_bg_ns["dolazak"][i] + '\n\n'

    bot.reply_to(message,reply_bg_ns)

@bot.message_handler(func=(lambda message : True if ("prognoza" in message.text) else False))
def prognoza(message):
    grad = message.text.strip('/prognoza ')
    weather_api = "33f0c1eacb7ef3c6cfe6b8a2ad84b23d"

    url = "https://api.openweathermap.org/data/2.5/weather?q=" + grad + " &appid="+ weather_api + "&lang=sr"


    vreme = requests.get(url).json()
    if int(vreme['cod']) == 404:
        bot.reply_to(message,"Није унешен иправан град")
        return

    kelvin = 273.15 
    temp = int(vreme['main']['temp'] - kelvin)
    humidity = vreme['main']['humidity']
    wind_speed = vreme['wind']['speed'] * 3.6
    formater = "{0:.2f}"
    wind_speed = formater.format(wind_speed)
    sunrise = vreme['sys']['sunrise']
    sunset = vreme['sys']['sunset']
    cloudy = vreme['clouds']['all']
    description = vreme['weather'][0]['description']
    sunrise = vremenzka_zona_konvert(sunrise)
    sunset = vremenzka_zona_konvert(sunset)

    bot.reply_to(message, "Време: " + description + "\n" + "Температура: " + str(temp) + " C°" "\n" + "Облачност: " + str(cloudy) + "%" +"\n" +"Влажност ваздуха: " + str(humidity) + "%\n" + "Излазак сунца: " + str(sunrise) + "\n" + "Залазак сунца: " + str(sunset) + "\n"
        + "Брзина ветра: " + str(wind_speed) + " km/h" + "\n")

def vremenzka_zona_konvert(utc):
    lokalno_vreme = datetime.datetime.fromtimestamp(utc)
    return lokalno_vreme.time().strftime("%H:%M")

bot.infinity_polling()