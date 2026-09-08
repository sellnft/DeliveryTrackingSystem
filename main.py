users = {
    "user1": "qwerty123",
    "user2": "qwerty456"
}

def render_menu():
    print("Добро пожаловать в систему")
    action = None
    while (action != "0"):
        print("Выберите дальнейшее действие:")
        print("1. Регистрация")
        print("2. Логин")
        print("0. Выход")
        action = input("> ")

        if (action != "1" and action != "2" and action != "0"):
            print("Некорректное действие")

        if (action == "1"):
            userName = input("Введите имя пользователя: ")
            password = input("Введите пароль: ")
            users[userName] = password

        if (action == "2"):
            userName = input("Введите имя пользователя: ")
            found = False

            for user in users.keys():
                if user == userName:
                    found = True
                    break

            if found == False:
                print("Некорректный пользователь")
            else:
                password = None
                while(password != "0"):
                
                    password = input("Введите пароль(нажмите 0 для выхода): ")
                    if check_password(userName, password) == False:
                        print("Некорректный пароль")
                    else: 
                        print("Пароль верен")
                        render_logged_menu()
                        break


def check_password(username: str, password_entered: str) -> bool:
    return users[username] == password_entered

def render_logged_menu():
    print("=====Выберите действие=====")
    print("1. Список пользователей")

    action = input("> ")
    if action == "1":
        for i in users:
            print(i, ": ", users[i])
        
render_menu()