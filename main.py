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

    def create_user(self, name: str, surname: str, age: int) -> str:
        self.users[self.last_id] = User(name, surname, age, self.last_id)
        self.update_id()
        return self.get_user_by_id(self.last_id - 1)

    def get_user_by_id(self, id: int) -> str:
        for user in self.users:
            if user == id:
                return self.users[user]
        else:
            return f'ОШИБКА: Пользователь с id: {id} не найден'

    def get_users_list(self) -> str:
        users_list = ''
        for user in self.users:
            users_list += f'''\nid пользователя: {self.users[user].id} \nИмя пользователя: {self.users[user].name}\nФамилия пользователя: {self.users[user].surname}\nВозраст пользователя: {self.users[user].age}\n'''
        return users_list

    def remove_user(self, user_id: int):
        self.users.pop(user_id)


class User():
    def __init__(self, name: str, surname: str, age: int, id: int):
        self.name = name
        self.surname = surname
        self.age = age
        self.id = id

    def __str__(self):
        return f'''\nid пользователя: {self.id} \nИмя пользователя: {self.name}\nФамилия пользователя: {self.surname}\nВозраст пользователя: {self.age}'''


if __name__ == '__main__':

    print('Добрый день! Вас приветствует сервачок'.center(60, '.'))
    print('''Перчень доступных комманд:
        1. get - Получить информацию о пользователе;
        2. add - Добавить пользователя;
        3. list - Получить список доступных пользователей;
        4. del - Удалить пользователя;
        5. stop - Завершение работы''')

    try:
        with open(r'./base/base_users', 'rb') as base:
            users_base = dill.load(base)
    except FileNotFoundError:
        users_base = Company()

    contr = True
    while contr:

        request = input('\nВведите запрос: ').lower()

        if request == 'stop':
            print('Good luck!')
            contr = False

        elif request == 'get':
            try:
                get_user_id = int(input('Введите id пользователя: '))
            except ValueError:
                print('ОШИБКА: ID пользователя должно быть числом')

            if get_user_id is not None:
                print(''.center(60, '.'))
                print('Результат запроса:')
                print(users_base.get_user_by_id(get_user_id))

        elif request == 'add':
            name = input('Введите имя пользователя: ')
            surname = input('Введите фамилию пользователя: ')
            try:
                age = int(input('Введите возраст пользователя: '))
            except ValueError:
                print('ОШИБКА: Возраст пользоваетля должен быть в числовом формате')

            if len(name) != 0 and len(surname) != 0:
                if 0 <= age <= 99:
                    print(''.center(60, '.'))
                    print(f'Пользователь {name} успешно добавлен в базу:')
                    print(users_base.create_user(name, surname, age))
                else:
                    print('ОШИБКА: Вы ввели не корректный формат возраста! Возраст может быть в диапазоне 0-99')
            else:
                print("ОШИБКА: Поля имя и фамилия не могут быть пустыми")

        elif request == 'list':
            print(''.center(60, '.'))
            print('Пользователи зарегестрированные в базе:')
            print(users_base.get_users_list(), end='')
            print(''.center(60, '.'))

        elif request == 'del':
            try:
                del_user_id = int(input('Введите id пользователя для удаления: '))
            except ValueError:
                print('ОШИБКА: ID пользователя должно быть числом')

            if del_user_id is not None:
                if del_user_id in users_base.users.keys():
                    agree = input(f"Вы уверенны что хотите удалить пользователя с id:{del_user_id}? [y/n]: ").lower()
                    if agree == 'y':
                        users_base.remove_user(del_user_id)
                        print(''.center(60, '.'))
                        print(f'Пользователь с id:{del_user_id} был успешно удален.')
                    elif agree == 'n':
                        print('Удаление было отмененно')
                    else:
                        print('ОШИБКА: Не корректная команда')
                else:
                    print(f'ОШИБКА: Пользователя с id:{del_user_id} нет в базе.')

        else:
            print('ОШИБКА: Вы ввели не корректиный запрос')

    with open(r'./base/base_users', 'wb') as base:
        dill.dump(users_base, base)
