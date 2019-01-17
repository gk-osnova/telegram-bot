# Path
LIB_FOLDER = "libs/"
LOG_FILE = "logs/chatbot.log"
EPD_FILE = "resources/epd.pdf"

# Token
TELEGRAM_TOKEN = "TELEGRAM TOKEN"

# States
CHOOSING_ACTION, REGISTRATION = range(2)


# Database data
DB_PORT = 3306
DB_HOST = "db_host"
DB_USER = "db_user"
DB_PASS = "user_pass"
DB_NAME = "telegram_bot_data"

# messages
COMMANDS = "Вот мои команды\n" \
           "/start - начало работы\n" \
           "/help - показать все команды\n" \
           "/restart - если что-то не работает"

GREETING_MESSAGE = "{}, приветствую Вас в Умном Доме ДомиУм!"

NEWS_MESSAGE = "Приветствую Вас в Канале Новостей!"

CONDOMINIUM_BILL_MESSAGE = "Приветствую Вас в ЖКХ ДомиУм!\nПолучите свой крайний ЕПД"

REGISTRATION_BADGE_MESSAGE = "Приветствую Вас в Гостях ДомиУм!"

SEND_VIDEO_MESSAGE = "Приветствую Вас в Видео ДомиУм!"

VIDEO_URL_MESSAGE = "http://www.legacyvet.com/sites/default/files/videos/Video%20%281%29.mp4"

HINT_MESSAGE = "Выбери действие по кнопке"

ENTER_ACCOUNT_MESSAGE = "Введите пожалуйста ваш счет"

START_MESSAGE = "Для продолжения работы нам нужно с вами познакомиться, нажмите на кнопку \"Зарегистрироваться\"\n"

NOT_TRUE_ACCOUNT_MESSAGE = "Не верно!\nПовторите еще раз."

SUCCESS_REGISTRATION_MESSAGE = "Ваш счет - {}\nПоздравляем с успешной регистрацией ! 👏👏👏"

# callback_data
callback_data_register_car = "register car"
callback_data_not_register_car = "not register car"
callback_data_register_visitor = "register visitor"
callback_data_not_register_visitor = "not register visitor"
