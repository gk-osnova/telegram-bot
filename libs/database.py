import MySQLdb
import constants


class Database:

    def __init__(self, logger):
        """init class database, fields: connection - connection to the database, logger - logging object"""
        self.connection = None
        self.logger = logger
    
    def connect_dbs(self):
        """initializes connections to the database"""
        if self.connection is not None:
            self.logger.info("Connection exists")
            return self.connection
        self.connection = MySQLdb.connect(constants.DB_HOST, constants.DB_USER, constants.DB_PASS, constants.DB_NAME)
        self.connection.ping(True)
        self.connection.autocommit(True)
        return self.connection
    
    def reconnect_dbs(self):
        """reconnection to the database"""
        self.logger.info("Delete older connection and reconnect")
        try:
            self.connection = None
            self.connection = MySQLdb.connect("localhost", "login", "pass", "db")
            self.connection.ping(True)
            self.connection.autocommit(True)
        except Exception as e:
            self.logger.error("Error reconnect_dbs()" + "\t" + str(e))

    def is_user_authorized(self, token):
        """
        :param token: user telegram-token.
        :return bool: if the user is authorized the function returns TRUE otherwise it returns FALSE.
        """
        try:
            cursor = self.connection.cursor()
            count = cursor.execute("SELECT * FROM telegram_users WHERE telegram_token = %s", (token, ))
            #self.logger.info("is_user_authorized() token - " + str(token) + " count - " + str(count))
            if count == 0:
                return False
            else:
                return True
        except Exception as e:
            self.logger.error("Error check is the user authorized " + "\t" + str(e))
            self.reconnect_dbs()

    def update_user_token(self, token, personal_account):
        """
        :param token: user telegram-token.
        :param personal_account: data entered by the user.
        :return: bool: if the operation is completed successfully it returns TRUE, otherwise it returns FALSE.
        Updates information about the user in the database.
        """
        try:
            cursor = self.connection.cursor()
            count = cursor.execute("UPDATE telegram_users SET telegram_token = %s WHERE personal_account = %s", (token, personal_account, ))
            #self.logger.info("update_user_token() token - " + str(token) + " personal account - " + str(personal_account) + " count - " + str(count))
            if count == 0:
                return False
            else:
                return True
        except Exception as e:
            self.logger.error("Error update user token " + "\t" + str(e))
            self.reconnect_dbs()

    def close_connection(self):
        """Close connection"""
        if self.connection is not None:
            self.connection.close()
