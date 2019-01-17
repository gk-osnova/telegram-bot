Telegram Chatbot v1.0
=============

Project Structure
=============================
start.py - the main telegram chatbot script
constants.py - the list of constant variables with tokens, DB connection parameters, bot messages and etc.
libs/chatbot.py - the chatbot implementation script
libs/database.py - the script for database management (get information about users, DB connection management, etc.)
db_generation/create_db.sql - the sql script for initial DB generation
logs/ - chatbot logs directory
resources/ - chatbot resources

REQUIREMENTS
=============================
The minimum requirements for the chatbot is Python v3.6.4 and the following Python external libraries:
	python-telegram-bot - wrapper for Telegram Bot API
	mysqlclient - module for working with MySQL database

INSTALLATION OF PYTHON LIBRARIES
=============================
pip install <module_name>

INSTALLATION OF MYSQL DATABASE ON LINUX
=============================
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo mysql_install_db
sudo apt-get install libmysqlclient-dev


 