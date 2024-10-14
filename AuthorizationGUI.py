import hashlib
import json
import os
import uuid
from tkinter import *
from tkinter.messagebox import showerror, showinfo


class Authorization:
    def __init__(self, root):
        self.root = root
        self.auth_init_ui()
        self.pass_dict = self.load_data()

    # Функция загрузки данных из файла
    def load_data(self):
        if os.path.exists('users.txt'):
            try:
                with open('users.txt', 'r') as users_file:
                    return json.load(users_file)
            except json.JSONDecodeError:
                return {}
        return {}

    # Функция сохранения данных в файл
    def save_data(self):
        with open('users.txt', 'w') as users_file:
            json.dump(self.pass_dict, users_file)

    # Регистрация нового пользователя
    def sign_up(self, login_entry, pass_entry):
        login = login_entry.get()
        password = pass_entry.get()

        if self.validate_input(login, password):
            if login in self.pass_dict:
                showerror('Error', 'You\'ve already authorised')
            else:
                salt = uuid.uuid4().hex
                password_hash = hashlib.md5((password + salt).encode()).hexdigest()
                self.pass_dict[login] = {'salt': salt, 'hash': password_hash}
                showinfo('Authorisation', 'Now you are authorised!')
                self.save_data()

    # Вход пользователя
    def sign_in(self, login_entry, pass_entry, messenger):
        login = login_entry.get()
        password = pass_entry.get()

        if self.sintax_check(login, password):
            if login not in self.pass_dict:
                showerror('Error', 'You\'ve not authorised')
            else:
                self.check_password(login, password, messenger)

    # Проверка пароля
    def check_password(self, login, password, messenger):
        stored_data = self.pass_dict[login]
        salt = stored_data['salt']
        password_hash = hashlib.md5((password + salt).encode()).hexdigest()

        if password_hash == stored_data['hash']:
            showinfo('Result', 'Password is correct, welcome!')
            messenger.main_page_init_ui()
        else:
            showerror('Result', 'Password is wrong, try again.')

    # Проверка синтаксиса ввода
    def sintax_check(self, login, password):
        if login.isalnum() and password.isalnum():
            return True
        showerror('Error', 'Syntax error in password or login')
        return False

    # Инициализация пользовательского интерфейса
    def auth_init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title('Messenger')
        self.root.geometry('450x600')
        self.root.resizable(False, False)
        self.root['bg'] = '#7dd5d2'

        Label(text='Login:', font='Sylfaen', background='White').place(x=30, y=205)
        Label(text='Password:', font='Sylfaen', background='White').place(x=30, y=285)

        # Поля для ввода логина и пароля
        self.login_entry = Entry(justify=LEFT, font='TimesNewRoman 11')
        self.login_entry.place(height=40, width=150, x=30, y=240)
        self.login_entry.focus()

        self.pass_entry = Entry(justify=LEFT, font='TimesNewRoman 11')
        self.pass_entry.place(height=40, width=150, x=30, y=320)

        # Кнопки
        Button(text='Sign in', font='Sylfaen', background='White', command=lambda: self.sign_in(self.login_entry, self.pass_entry, self)).place(height=30, width=90, x=210, y=260)
        Button(text='Sign up', font='Sylfaen 12', background='White', command=lambda: self.sign_up(self.login_entry, self.pass_entry)).place(height=25, width=80, x=215, y=310)

    def main_page_init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title('Forums')
        self.root['bg'] = 'White'

        self.forum_list = Listbox(self.root, font='TimesNewRoman 12', height=10)
        self.forum_list.pack(pady=20, padx=20)

        # Добавление форумов в список
        self.forum_list.insert(END, 'Forum 1')
        self.forum_list.insert(END, 'Forum 2')
        self.forum_list.insert(END, 'Forum 3')

        self.message_entry = Entry(self.root, justify=LEFT, font='TimesNewRoman 11')
        self.message_entry.pack(pady=10, padx=20)

        send_button = Button(self.root, text='Send')
        send_button.pack(pady=10)

        logout_button = Button(self.root, text='Logout', command=self.auth_init_ui)
        logout_button.pack(pady=10)


if __name__ == "__main__":
    root = Tk()
    app = Authorization(root)
    root.mainloop()
