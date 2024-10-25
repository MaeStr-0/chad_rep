
import sqlite3
import string
import asyncio

async def existence_check(username):
    try:
        print("Процесс - существует ли такой пользователь?")
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()
        exist_check = "SELECT COUNT(*) FROM credentials WHERE username = ?;"
        data = [(username)]
        answer = cursor.execute(exist_check, data).fetchone()[0]
        print(answer)
        if answer == 1:
            print("exist")
            cursor.close()
            return "exist"
        else:
            print("not_exist")
            cursor.close()
            return "not_exist"
    except:
        return "server_not_responding"
    finally:
        return "process_finished"




async def register(username, password):
    try:
        print('Процесс - регистрация пользователя')
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к test.db")
        exist_check = "SELECT COUNT(*) FROM credentials WHERE username = ?;"
        data = [(username)]
        answer = cursor.execute(exist_check, data).fetchone()[0]
        print(answer)
        if answer == 0:
            inserter = "INSERT INTO credentials VALUES(?, ?);"
            data = (username,password)
            print(data)
            back=cursor.execute(inserter, data)
            print(back.fetchone())
            print("Регистрация успешна")
            sqlite_connection.commit()
            t=cursor.execute("SELECT * FROM credentials;").fetchall()
            print(t)
            return 1

        else:
            print("Логин занят")
            sqlite_connection.commit()
            getter = "SELECT * FROM credentials;"
            t=cursor.execute(getter).fetchall()
            print(f"All data {t}")
            return 0

    except:
        print("Not")

    finally:
        print("smthng")



async def auth(username, pwd):
    try:
        print('Процесс - аутентификация')
        sqlite_connection = sqlite3.connect('test.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        sqlite_finder = "SELECT COUNT(*) FROM credentials WHERE username = ?;"
        data =[(username)]
        answer = cursor.execute(sqlite_finder, data).fetchone()[0]
        print(answer)
        if answer == 1:
            print("Данные найдены")
            passw_verify = "SELECT password FROM credentials WHERE username = ?;"
            verify = cursor.execute(passw_verify, data).fetchone()[0]
            print("This is verify",verify)
            if pwd == verify:
                 print("success")
                 return 1
                 sqlite_connection.commit()
                 
            else:
                 return 0
                 print("lose")
                 sqlite_connection.commit()
                 cursor.close()
        else:
            print("Данные не найдены")
            return 0
            sqlite_connection.commit()
            cursor.close()

        print("end")

 
    except:
        print("Исключение")
        return 0
    finally:
        if sqlite_connection:
          #sqlite_connection.close()
           print('Процесс завершен')


'''
async def main():
    await register("user123","uiop")
    await auth("user123","uiop") 
    await existence_check("user123")
'''
#register("user123","uiop")
#auth("user123","uiop")
#existence_check("user123")
