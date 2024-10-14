import hashlib
import json
import os
import uuid
from tkinter import *
from tkinter.messagebox import showerror, showinfo

from Publication import Publication


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

        if self.sintax_check(login, password):
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
            self.username = login
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
        self.root['bg'] = 'Blue'

        self.forum_list = Frame(self.root, height=100, width=450)
        self.forum_list.pack(pady=20, padx=20)

        add_forum_button = Button(self.root, text='Add forum', command=self.add_forum)
        add_forum_button.pack(pady=10)

        logout_button = Button(self.root, text='Logout', command=self.auth_init_ui)
        logout_button.pack(pady=10)

    def add_forum(self):
        add_window = Toplevel(self.root)
        add_window.title('Add forum')
        Label(add_window, text='Enter forum\'s name:').pack(pady=10)
        new_name_entry = Entry(add_window)
        new_name_entry.pack(pady=10)



    def save_publication(self, text, forum_name):
        new_publ = Publication(self.username, text)
        new_publ.save_data(forum_name)
        self.publication_list.insert(END, f'{self.username}: {text}')

    def forum_page(self, forum_name):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.title(forum_name)
        self.root['bg'] = 'White'
        self.publication_list = Listbox(self.root, font='Sylfaen', height=10, width=400)
        self.publication_list.pack(pady=20, padx=20)

        if os.path.exists('published.txt'):
            try:
                with open('published.txt', 'r') as published_file:
                    content = published_file.read().strip()
                    if content != '':
                        prev_publ = json.loads(content)
                        empty_flag = 1
                    else:
                        empty_flag = 0
            except (json.JSONDecodeError, FileNotFoundError):
                prev_publ = {}

        if empty_flag:
            for user, publications in prev_publ.items():
                for publication, publication_forum_name in publications:
                    if forum_name == publication_forum_name:
                        self.publication_list.insert(END, f'{user}: {publication}')

        entry = Entry(self.root)
        entry.pack(pady=10)

        enter_button = Button(self.root, text='Enter', command=lambda: self.save_publication(entry.get(), forum_name))
        enter_button.pack(pady=0, padx=20)

        back_button = Button(self.root, text='Back', command=self.main_page_init_ui)
        back_button.pack(pady=10)

        logout_button = Button(self.root, text='Logout', command=self.auth_init_ui)
        logout_button.pack(pady=10)


if __name__ == "__main__":
    root = Tk()
    app = Authorization(root)
    root.mainloop()
