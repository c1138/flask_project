import sqlite3

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print("Ошибка чтения из БД: " + str(e))
        return []

    def addUser(self, username, email, password_hash):
        try:
            self.__cur.execute("SELECT COUNT() as `count` FROM users WHERE email LIKE ?", (email,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            self.__cur.execute(
                "INSERT INTO users (username, email, password_hash, is_psychologist, profile_image, bio, qualification, experience, created_at, updated_at) VALUES (?, ?, ?, 0, '', '', '', '', datetime('now'), datetime('now'))",
                (username, email, password_hash)
            )
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД: " + str(e))
            return False

        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute("SELECT * FROM users WHERE user_id = ? LIMIT 1", (user_id,))
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД: " + str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute("SELECT * FROM users WHERE email = ? LIMIT 1", (email,))
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False

            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД: " + str(e))

        return False
