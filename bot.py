

import logging
import telegram
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os
from telegram.ext import BaseFilter
import airtable
import array

dkeybaord = []


tkeybaord =  [[InlineKeyboardButton("GC", callback_data='GC'),
              InlineKeyboardButton("FMG", callback_data='FMG')]]

skeyboard = [
             [InlineKeyboardButton("View Order", callback_data='VO')],
             [InlineKeyboardButton("Confirm Order", callback_data='CO')],
             [InlineKeyboardButton("Cancel Order", callback_data='CA')]

             ]

orderlinenum = 0
linepos = 920
totalpos = 400
ordertotal = 0
ordernum = 0
channelid = '-1001256710784'


class CardFilter(BaseFilter):
    def filter(self, message):
        return 'Patient Card 👀' in message.text


# Remember to initialize the class.
card_filter = CardFilter()


class MenuFilter(BaseFilter):
    def filter(self, message):
        return 'Menu 🥦' in message.text


# Remember to initialize the class.
menu_filter = MenuFilter()


class GetsomeFilter(BaseFilter):
    def filter(self, message):
        return 'Get Some 🥦' in message.text


# Remember to initialize the class.
gs_filter = GetsomeFilter()


class ContactFilter(BaseFilter):
    def filter(self, message):
        return 'Contact Us 📱' in message.text


# Remember to initialize the class.
contact_filter = ContactFilter()


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Keyboard


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    keyboard = [[KeyboardButton("Menu 🥦"),
                 KeyboardButton("Get Some 🥦")], [KeyboardButton("Contact Us 📱")], [KeyboardButton("Patient Card 👀")]]

    # [InlineKeyboardButton("Option 3", callback_data='3')]]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)





def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def card(update, context):
    """Card Handler"""
    update.message.reply_text("Creating Card..")
    cardtext = update.message.from_user.first_name + \
        " " + update.message.from_user.last_name
    filename = "./Cards/" + update.message.from_user.username + ".png"
    createcard(cardtext, "./Cards/" +
               update.message.from_user.username + ".png")
    update.message.reply_photo(open(str(filename), 'rb'))


def contact(update, context):
    """Contact Handler"""
    bot = telegram.Bot('844500002:AAHEwaD_cEZfpFLFxzcISTpocUXvPKeDS2A')
    update.message.reply_text(
        "Thank you for contacting us a representative will be in contact soon via telegram")
    contactmessage = "Contact Alert From " + update.message.from_user.first_name + " " + \
        update.message.from_user.last_name + \
        "(@" + update.message.from_user.username + ")"
    # bot.forward_message('-1001256710784',update.message.chat_id,update.message.message_id)
    bot.send_message(channelid, contactmessage)


def getsome(update, context):
    """Contact Handler"""
    #bot = telegram.Bot('844500002:AAHEwaD_cEZfpFLFxzcISTpocUXvPKeDS2A')
    update.message.reply_text(
        "Hi " + update.message.from_user.first_name + ".Click on Strain Code to add to order")
    #update.message.reply_text("Hi " + update.message.from_user.first_name + ".Feel free to check out the  MENU if you have not done so already . If you are ready please type in your order in the following format : The word <b>ORDER</b> followed by the code and quantity e.g order GC 3 , TW 4",parse_mode = 'HTML')
    update.message.reply_photo(open(str('./ESD/Menu.png'), 'rb'))

    reply_markup = InlineKeyboardMarkup(dkeybaord)

    update.message.reply_text('Select Strains:', reply_markup=reply_markup)


def menu(update, context):
    update.message.reply_text("Creating Menu..")
    createmenu()
    update.message.reply_photo(open(str('./ESD/Menu.png'), 'rb'))


def buildstrains():
    global dkeybaord
    i=0
    line1 = []
    line2 = []
    line3 = []
    menutable = airtable.Airtable(
        'appgc7FHhYjQlaEb5', 'STRAINS', api_key='keyIksztaSYNrh8FP')
    for page in menutable.get_iter(view='Grid 2', sort='Code'):
        for record in page:
            code = record['fields']['Code']
            kb = InlineKeyboardButton(str(code), callback_data=code)
            i= i+1
         
            if i < 6:
                line1.append(kb)
            if 6 <= i <= 10:
                line2.append(kb)
            if i > 10:
                line3.append(kb)
        
        dkeybaord.append(line1)
        dkeybaord.append(line2)
        dkeybaord.append(line3)

        spacer = [InlineKeyboardButton("[ACTIONS]", callback_data='xx')]
        vo = [InlineKeyboardButton("View Order", callback_data='VieOr')]
        co = [InlineKeyboardButton("Confirm Order", callback_data='ConOr')]
        ca = [InlineKeyboardButton("Cancel Order", callback_data='CanOr')]

        dkeybaord.append(spacer)
        dkeybaord.append(vo)
        dkeybaord.append(co)
        dkeybaord.append(ca)

    


def createmenu():
    menutable = airtable.Airtable(
        'appgc7FHhYjQlaEb5', 'STRAINS', api_key='keyIksztaSYNrh8FP')
    img = Image.open('./ESD/MenuT.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./fonts/Aaargh.ttf", 40)
    x = 150
    for page in menutable.get_iter(view='Grid 2', sort='Code'):
        for record in page:

            x = x + 80
            code = record['fields']['Code']
            draw.text((100, x), code, (0, 0, 0), font=font)
            name = record['fields']['Name']
            draw.text((550, x), name, (0, 0, 0), font=font)
            price = record['fields']['Price']
            draw.text((1400, x), price, (0, 0, 0), font=font)
    img.save('./ESD/Menu.png')


def createinvoiceline(code, username):
    invoicetable = airtable.Airtable(
        'appgc7FHhYjQlaEb5', 'STRAINS', api_key='keyIksztaSYNrh8FP')
    global orderlinenum
    global linepos
    global ordertotal
    if orderlinenum == 0:
        img = Image.open('./Invoices/invoiceT.png')
    else:
        img = Image.open('./Invoices/invoice.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./fonts/Aaargh.ttf", 20)
    #get other info
    line = invoicetable.search('Code', code)                                                   
    draw.text((120, linepos), code, (0, 0, 0), font=font)
    draw.text((170, linepos), line[0]['fields']['Name'], (0, 0, 0), font=font)
    draw.text((700, linepos), "1 (pc)", (0, 0, 0), font=font)
    draw.text((1000, linepos), " R " + line[0]['fields']['RPrice'], (0, 0, 0), font=font)
    orderlinenum = orderlinenum+1
    ordertotal =  ordertotal + int(line[0]['fields']['RPrice'])
    linepos = linepos + 40
    img.save('./Invoices/invoice.png')



def confirminvoice():
    invoicetable = airtable.Airtable(
    'appgc7FHhYjQlaEb5', 'STRAINS', api_key='keyIksztaSYNrh8FP')
    global orderlinenum
    global linepos
    global ordertotal
    if orderlinenum == 0:
        img = Image.open('./Invoices/invoiceT.png')
    else:
        img = Image.open('./Invoices/invoice.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./fonts/Aaargh.ttf", 20)
    #get other info
    draw.text((1000, 1410), " R "+ str(ordertotal), (0, 0, 0), font=font)
    img.save('./Invoices/invoice.png')


def createcard(pname, filename):
    """Build Card"""
    img = Image.open("./Cards/pcard.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./fonts/Aaargh.ttf", 40)
    draw.text((50, 150), pname, (0, 0, 0), font=font)
    img.save(filename)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def button(update, context):
    query = update.callback_query
    bot = telegram.Bot('844500002:AAHEwaD_cEZfpFLFxzcISTpocUXvPKeDS2A')
    uid = update.callback_query.from_user.id
    reply_markup = InlineKeyboardMarkup(dkeybaord)

    if query.data == "VieOr":
        bot.send_photo(uid,open(str('./Invoices/invoice.png'), 'rb'))
        bot.send_message(uid, "Add More", reply_markup=reply_markup)
        return

    if query.data == "ConOr":
        confirminvoice()
        bot.send_photo(uid,open(str('./Invoices/invoice.png'), 'rb'))
        bot.send_message(uid, "Order confirm for R " + str(ordertotal), reply_markup=reply_markup)
        bot.send_message(channelid,"Order from " + update.callback_query.from_user.name)
        bot.send_photo(channelid,open(str('./Invoices/invoice.png'), 'rb'))

        return

    createinvoiceline(query.data, "gg")
    query.edit_message_text(text="{} Added to Order: Curent Total: R {}".format(query.data,str(ordertotal)))
    
    bot.send_message(uid, "Add More", reply_markup=reply_markup)


def main():
    """Start the bot."""

    #strains = menutable.get_all(view='StrainView',sort='Code')
    skeyboard = [[InlineKeyboardButton("GC", callback_data='GC'),
                  InlineKeyboardButton("FMG", callback_data='FMG')],

                 [InlineKeyboardButton("View Order", callback_data='VO')]]
    bot = telegram.Bot('844500002:AAHEwaD_cEZfpFLFxzcISTpocUXvPKeDS2A')
    updater = Updater(
        "844500002:AAHEwaD_cEZfpFLFxzcISTpocUXvPKeDS2A", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # updater.dispatcher.add_handler(CallbackQueryHandler(button))

    dp.add_handler(MessageHandler(card_filter, card))
    dp.add_handler(MessageHandler(menu_filter, menu))
    dp.add_handler(MessageHandler(contact_filter, contact))
    dp.add_handler(MessageHandler(gs_filter, getsome))
    dp.add_handler(CallbackQueryHandler(button))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # createmenu()
    buildstrains()
    main()
