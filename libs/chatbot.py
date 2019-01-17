        #-*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import re
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)
import constants
import database


class CommandProcessor(object):

    def __init__(self, logger):
        """

        :param logger:
        initialize buttons
        """
        self.logger = logger
        self.for_registered_keyboard = [["Гости", "ЖКХ"], ["Видео", "Канал новостей"]]
        self.for_unregistered_keyboard = [["Зарегистрироваться"]]
        self.pass_for_car_keyboard = [[InlineKeyboardButton("Регистрировать", callback_data=constants.callback_data_register_car), InlineKeyboardButton("Отмена", callback_data=constants.callback_data_not_register_car)]]
        self.pass_for_visitor_keyboard = [[InlineKeyboardButton("Регистрировать", callback_data=constants.callback_data_register_visitor), InlineKeyboardButton("Отмена", callback_data=constants.callback_data_not_register_visitor)]]
        self.pass_for_visitor_markup = InlineKeyboardMarkup(self.pass_for_visitor_keyboard, one_time_keyboard=True)
        self.pass_for_car_markup = InlineKeyboardMarkup(self.pass_for_car_keyboard, one_time_keyboard=True)
        self.for_registered_markup = ReplyKeyboardMarkup(self.for_registered_keyboard, one_time_keyboard=True)
        self.for_unregistered_markup = ReplyKeyboardMarkup(self.for_unregistered_keyboard, one_time_keyboard=True)
        #initialization

    def error_handler(self, bot, update, error):
        """The function that triggers on error"""
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def command_info(self, bot, update):
        """The function that is triggered when entering a command '/help' """
        update.message.reply_text(constants.COMMANDS)

    def start(self, bot, update):
        """
        :param bot:
        :param update:
        :return State:
        The function triggers when the bot restarts, or when the user activates the bot at first time.
        Checks the telegram token and detects if the bot knows the user.
        If bot knows the user it will suggest to select the action from the menu. Otherwise the user goes to the REGISTRATION state.
        """
        user_id = update.message.chat.id
        #self.logger.info("start() token - " + str(user_id))
        db = database.Database(self.logger)
        db.connect_dbs()
        is_user_authorized = db.is_user_authorized(user_id)
        db.close_connection()
        if is_user_authorized == True:
            update.message.reply_text(
                constants.GREETING_MESSAGE.format(update.message.chat.first_name),
                reply_markup=self.for_registered_markup)
            update.message.reply_text(
                constants.COMMANDS,
                reply_markup=self.for_registered_markup)
            return constants.CHOOSING_ACTION

        else:
            update.message.reply_text(
                constants.START_MESSAGE,
                reply_markup=self.for_unregistered_markup)
            return constants.REGISTRATION

    def registration_step_two(self, bot, update, user_data):
        """
        :param bot:
        :param update:
        :param user_data:
        :return State:
        The function is triggered when the user enters a message at the registration state.
        If the personal account is correct, the bot suggests the user to select the action and user goes to the CHOOSING_ACTION state.
        """
        user_id = update.message.chat.id
        personal_account = update.message.text
        db = database.Database(self.logger)
        db.connect_dbs()
        is_success = db.update_user_token(user_id, personal_account)
        db.close_connection()
        if is_success == True:
            self.logger.info("registration() token - " + str(user_id) + " success")
            update.message.reply_text(
                constants.SUCCESS_REGISTRATION_MESSAGE.format(personal_account),
                reply_markup=self.for_registered_markup)
            return constants.CHOOSING_ACTION
        else:
            self.logger.info("registration() token - " + str(user_id) + " not success")
            if user_data.get("button_register_press") == "Зарегистрироваться":
                update.message.reply_text(
                    constants.NOT_TRUE_ACCOUNT_MESSAGE
                )
                return constants.REGISTRATION
            else:
                update.message.reply_text(
                    "Для продолжения нажмите на кнопку \"Зарегистрироваться\""
                )
                return constants.REGISTRATION

    def registration_step_one(self, bot, update, user_data):
        """
        :param bot:
        :param update:
        :param user_data:
        :return: State
        The function is triggered when the user enters the registration state at first time.
        If the user clicks on the register button, the bot saves this action and proposes to enter the account information.
        """
        data = update.message.text
        if data == "Зарегистрироваться" and user_data.get("button_register_press") is None:
            user_data["button_register_press"] = data
        update.message.reply_text(
            constants.ENTER_ACCOUNT_MESSAGE
        )
        return constants.REGISTRATION

    def get_news(self, bot, update, user_data):
        """
        :param bot:
        :param update:
        :param user_data:
        :return: State
        Get news function.
        Returns user to the action selection state - "CHOOSING_ACTION".
        """
        #self.logger.info("get_news() token - " + str(update.message.chat.id))
        update.message.reply_text(
            constants.NEWS_MESSAGE,
            reply_markup=self.for_registered_markup
        )
        return constants.CHOOSING_ACTION

    def get_condominium_bill(self, bot, update, user_data):
        """
        :param bot:
        :param update:
        :param user_data:
        :return: State
        Returns the last bill to the user.
        Returns user to the action selection state - "CHOOSING_ACTION"
        """
        #self.logger.info("get_condominium_bill() token - " + str(update.message.chat.id))
        update.message.reply_text(constants.CONDOMINIUM_BILL_MESSAGE)
        bot.send_document(chat_id=update.message.chat_id, document=open(constants.EPD_FILE, "rb"),
                          reply_markup=self.for_registered_markup)
        return constants.CHOOSING_ACTION

    def get_video(self, bot, update, user_data):
        """
        :param bot:
        :param update:
        :param user_data:
        :return: State
        Returns link to the last video file from the video storage
        Returns user to the action selection state - "CHOOSING_ACTION"
        """
        #self.logger.info("get_video() token - " + str(update.message.chat.id))
        update.message.reply_text(constants.SEND_VIDEO_MESSAGE)
        bot.send_video(chat_id=update.message.chat_id,
                       video=constants.VIDEO_URL_MESSAGE,
                       reply_markup=self.for_registered_markup)
        return constants.CHOOSING_ACTION

    def registration_badge(self, bot, update, user_data):
        """
        :param bot:
        :param update:
        :param user_data:
        :return: State
        Returns registration badge message.
        Returns user to the action selection state - "CHOOSING_ACTION"
        """
        self.logger.info("registration_badge() token - " + str(update.message.chat.id))
        update.message.reply_text(
            constants.REGISTRATION_BADGE_MESSAGE,
            reply_markup=self.for_registered_markup
        )
        return constants.CHOOSING_ACTION

    def all_message(self, bot, update, user_data):
        """
        :param bot:
        :param update:
        :param user_data:
        :return: State
        The function is called for different user messages.
        Checks telephone numbers by the regular expression.
        Checks car numbers by the regular expression.
        """
        text = update.message.text
        #self.logger.info("all_message() token - " + str(update.message.chat.id) + " data - " + text)
        car_number = re.findall('[a-zА-Яа-яА-Я]\d{3}[a-zА-Яа-яА-Я]{2}\d{2,3}', text)
        telephone_number = re.findall('8[0-9]{10}', text)
        user_data["data"] = text
        if len(car_number) != 0:
            update.message.reply_text(
                "Заказать пропуск на автомобиль  " + text + "?",
                reply_markup=self.pass_for_car_markup)
        elif len(telephone_number) != 0:
            update.message.reply_text(
                "Выслать пропуск посетителю на телефон " + text + "?",
                reply_markup=self.pass_for_visitor_markup)
        else:
            update.message.reply_text(
                constants.HINT_MESSAGE,
                reply_markup=self.for_registered_markup)
            return constants.CHOOSING_ACTION

    def call_back_query(self, bot, update, user_data):
        """
        :param bot:
        :param update:
        :return: State
        The function is called when the button is pressed in the inline keyboard.
        Checks pressed button names on the callback_data and selects the appropriate action.
        """
        text = data = user_data["data"]
        data = update.callback_query.data
        if data == constants.callback_data_register_car:
            bot.send_message(chat_id=update.callback_query.message.chat.id, text="Пропуск на машину заказан!", reply_markup=self.for_registered_markup)
        elif data == constants.callback_data_not_register_car:
            bot.send_message(chat_id=update.callback_query.message.chat.id, text="Пропуск не заказан!", reply_markup=self.for_registered_markup)
        elif data == constants.callback_data_register_visitor:
            bot.send_message(chat_id=update.callback_query.message.chat.id, text="QR пропуск выслан на телефон!", reply_markup=self.for_registered_markup)
        elif data == constants.callback_data_not_register_visitor:
            bot.send_message(chat_id=update.callback_query.message.chat.id, text="Пропуск не заказан!", reply_markup=self.for_registered_markup)
        return constants.CHOOSING_ACTION
        

class Bot(object):
    def __init__(self, logger):
        """
        :param logger:
        Initialize the command processor.
        Creation of the list of handlers.
        Initialization of the states and handlers in the states.
        """
        self.command_processor = CommandProcessor(logger)
        self.updater = Updater(constants.TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.command_processor.start), CommandHandler('restart', self.command_processor.start)],
            states={
                constants.CHOOSING_ACTION: [
                    # If we are in this state, then our message will be processed by one of these handlers, or by a global handler
                    # https://python-telegram-bot.readthedocs.io/en/stable/telegram.ext.conversationhandler.html
                    RegexHandler('^(Гости)$', self.command_processor.registration_badge, pass_user_data=True),
                    RegexHandler('^(ЖКХ)$', self.command_processor.get_condominium_bill, pass_user_data=True),
                    RegexHandler('^(Видео)$', self.command_processor.get_video, pass_user_data=True),
                    RegexHandler('^(Канал новостей)$', self.command_processor.get_news, pass_user_data=True),
                    MessageHandler(Filters.text, self.command_processor.all_message, pass_user_data=True)
                ],
                constants.REGISTRATION: [
                    RegexHandler('^(Зарегистрироваться)$', self.command_processor.registration_step_one, pass_user_data=True),
                    MessageHandler(Filters.text, self.command_processor.registration_step_two, pass_user_data=True)
                ]
            },
            fallbacks=[CommandHandler('start', self.command_processor.start), CommandHandler('restart', self.command_processor.start)]
        )
        self.dispatcher.add_handler(CommandHandler('help', self.command_processor.command_info))
        self.dispatcher.add_handler(CallbackQueryHandler(self.command_processor.call_back_query, pass_user_data=True))
        self.dispatcher.add_handler(self.conversation_handler)
        self.dispatcher.add_error_handler(self.command_processor.error_handler)
        #chatbot initialization
        
    def process_request(self):
        self.updater.start_polling()
        self.updater.idle()
        #process user requests
