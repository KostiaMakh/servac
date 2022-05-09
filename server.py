import dill


class Company():
    last_id = 1
    users = {}

    def __getstate__(self) -> dict:
        state = {}
        state["last_id"] = self.last_id
        state["users"] = self.users
        return state

    def __setstate__(self, state: dict):
        self.users = state["users"]
        self.last_id = state["last_id"]

    def update_id(self):
        self.last_id += 1

    def add_user(self, name, surname, age):
        self.users[self.last_id] = User(name, surname, age, self.last_id)
        self.update_id()
        return self.get_user_by_id(self.last_id - 1)

    def get_user_by_id(self, id):
        for user in self.users:
            if user == id:
                return self.users[user]
        else:
            return f'ОШИБКА: Пользователь с id: {id} не найден'

    def get_users_list(self):
        users_list = ''
        for user in self.users:
            users_list += f'''\nid пользователя: {self.users[user].id} \nИмя пользователя: {self.users[user].name}\nФамилия пользователя: {self.users[user].surname}\nВозраст пользователя: {self.users[user].age}\n'''
        return users_list

    def remove_user(self, user_id):
        self.users.pop(user_id)


class User():
    def __init__(self, name, surname, age, id):
        self.name = name
        self.surname = surname
        self.age = age
        self.id = id

    def __str__(self):
        return f'''\nid пользователя: {self.id} \nИмя пользователя: {self.name}\nФамилия пользователя: {self.surname}\nВозраст пользователя: {self.age}'''


def exit_control(req):
    if req == 'stop':
        return False
    else:
        return True

with open(r'base_users', 'rb') as base:
    users_base = dill.load(base)

print('Добрый день! Вас приветствует сервачок'.center(60, '.'))
print('''Перчень доступных комманд:
    1. get - Получить информацию о пользователе;
    2. add - Добавить пользователя;
    3. list - Получить список доступных пользователей;
    4. del - Удалить пользователя;
    5. stop - Завершение работы''')

contr = True
while contr == True:
    request = input('\nВведите запрос: ').lower()
    contr = exit_control(request)

    if request == 'get':
        try:
            user_id = input('Введите id пользователя: ')
            contr = exit_control(user_id)
            user_id = input(user_id)
            if user_id is not None:
                print(''.center(60, '.'))
                print('Результат запроса:')
                print(users_base.get_user_by_id(user_id))
        except:
            print('ОШИБКА: ID пользователя должно быть числом')

    elif request == 'add':
        name = input('Введите имя пользователя: ')
        contr = exit_control(name)
        surname = input('Введите фамилию пользователя: ')
        contr = exit_control(surname)
        try:
            age = input('Введите возраст пользователя: ')
            contr = exit_control(age)
            age = int(age)
            if name.__len__() != 0 and surname.__len__() != 0:
                if 0 <= age <= 99:
                    print(''.center(60, '.'))
                    print(f'Пользователь {name} успешно добавлен в базу:')
                    print(users_base.add_user(name, surname, age))
                else:
                    print('ОШИБКА: Вы ввели не корректный формат возраста!\nВозраст может быть в диапазоне 0-99')
            else:
                print("ОШИБКА: Поля имя и фамилия не могут быть пустыми")
        except:
            print('ОШИБКА: Возраст пользоваетля должен быть в числовом формате')


    elif request == 'list':
        print(''.center(60, '.'))
        print('Пользователи зарегестрированные в базе:')
        print(users_base.get_users_list(), end='')
        print(''.center(60, '.'))

    elif request == 'del':
        try:
            user_id = input('Введите id пользователя для удаления: ')
            contr = exit_control(user_id)
            user_id = int(user_id)
            if user_id is not None:
                if user_id in users_base.users.keys():
                    agree = input(f"Вы уверенны что хотите удалить пользователя с id:{user_id}? [y/n]: ").lower()
                    contr = exit_control(agree)
                    if agree == 'y':
                        users_base.remove_user(user_id)
                        print(''.center(60, '.'))
                        print(f'Пользователь с id:{user_id} был успешно удален.')
                    elif agree == 'n':
                        print('Удаление было отмененно')
                    else:
                        print('ОШИБКА: Не корректная команда')
                else:
                    print(f'ОШИБКА: Пользователя с id:{user_id} нет в базе.')
        except:
            print('ОШИБКА: ID пользователя должно быть числом')

    elif contr == False:
        print('Пока!')

    else:
        print('ОШИБКА: Вы ввели не корректиный запрос')

with open(r'base_users', 'wb') as base:
    dill.dump(users_base, base)

