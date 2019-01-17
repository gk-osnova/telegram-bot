#-*- coding: utf-8 -*-
import sys
import constants
import logging
sys.path.append(constants.LIB_FOLDER)
import chatbot
import database

def main():
    """
    Initializing the Logger
    Create the bot object
    Start listening the bot channel
    """
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO, filename=constants.LOG_FILE)
    logger = logging.getLogger(__name__)
    bot = chatbot.Bot(logger)
    bot.process_request()


if __name__ == '__main__':
    main()
