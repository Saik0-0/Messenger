import hashlib
import json
import os
import uuid
from datetime import datetime
from functools import partial
from tkinter import *
from tkinter.messagebox import showerror, showinfo

from Publication import Publication


class Authorization:
    def __init__(self, root):
        self.root = root
        self.auth_init_ui()
        self.pass_dict = self.load_data()

    # Функция загрузки логинов и паролей из файла
    def load_data(self):
        if os.path.exists('users.txt'):
            try:
                with open('users.txt', 'r') as users_file:
                    return json.load(users_file)
            except json.JSONDecodeError:
                return {}
        return {}

    # Функция сохранения логинов и паролей в файл
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

    # Проверка введённого пароля если пользователь авторизован
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

    #   Функция сохранения публикации
    def save_publication(self, text, forum_name):
        publ_time = datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        new_publ = Publication(self.username, text, forum_name, publ_time)
        new_publ.save_data()
        #   добавляем публикацию в Listbox
        self.publication_list.insert(END, f'[{new_publ.time}] {new_publ.username}: {new_publ.text} (Likes: {new_publ.likes})')
        for comment in new_publ.comments:
            self.publication_list.insert(END, f'    Comment: {comment}')

    #   Функция загрузки данных о публикациях из файла
    def load_publications(self):
        if os.path.exists('published.txt'):
            try:
                with open('published.txt', 'r') as published_file:
                    content = published_file.read().strip()
                    if content:
                        return json.loads(content)
            except json.JSONDecodeError:
                return {}
        return {}

    #   Функция сохранения данных о публикациях в файл
    def save_publications(self, data):
        with open('published.txt', 'w') as published_file:
            json.dump(data, published_file)

    #   Функция добавления лайка
    def like_post(self, forum_name):
        selected = self.publication_list.curselection()
        if selected:
            index = selected[0]
            #   Загружаем данные публикаций из файла, добавляем в
            #   список публикации из нужного форума и сортируем по времени
            prev_publ_dict = self.load_publications()
            prev_publ_tuples = []
            for user, publications in prev_publ_dict.items():
                for publication in publications:
                    if forum_name == publication['forum_name']:
                        prev_publ_tuples.append((
                            user, publication['text'], publication['forum_name'],
                            publication['time'], publication['likes'], publication['comments']
                        ))
            prev_publ = sorted(prev_publ_tuples, key=lambda x: x[3])

            #   Находим в списке и в файле нужную публикацию через индекс в Listbox, обновляем данные
            real_index = 0
            for i, (user, text, _, time, likes, comments) in enumerate(prev_publ):
                if real_index == index:
                    # Найдена нужная публикация, увеличиваем лайки
                    for orig_user, publications in prev_publ_dict.items():
                        for publication in publications:
                            if publication['text'] == text and publication['time'] == time and publication['likes'] == likes:
                                publication['likes'] += 1
                                # Обновляем отображение в списке
                                self.publication_list.delete(index)
                                self.publication_list.insert(index, f"[{publication['time']}] {user}: {publication['text']} (Likes: {publication['likes']})")
                                # Сохраняем обновленные данные
                                self.save_publications(prev_publ_dict)
                                return
                # Увеличиваем счетчик строк, добавляем одну строку за публикацию и столько строк,
                # сколько комментариев под ней
                real_index += (1 + len(comments))

    #   Функция добавления комментария
    def add_comment(self, comment_text, forum_name):
        selected = self.publication_list.curselection()
        if selected:
            index = selected[0]
            #   Загружаем данные публикаций из файла, добавляем в
            #   список публикации из нужного форума и сортируем по времени
            prev_publ_dict = self.load_publications()
            prev_publ_dict = self.load_publications()
            prev_publ_tuples = []
            for user, publications in prev_publ_dict.items():
                for publication in publications:
                    if forum_name == publication['forum_name']:
                        prev_publ_tuples.append((
                            user, publication['text'], publication['forum_name'],
                            publication['time'], publication['likes'], publication['comments']
                        ))
            prev_publ = sorted(prev_publ_tuples, key=lambda x: x[3])

            #   Находим в списке и в файле нужную публикацию через индекс в Listbox, обновляем данные
            real_index = 0
            for i, (user, text, _, time, likes, comments) in enumerate(prev_publ):
                if real_index == index:
                    # Найдена нужная публикация, добавляем комментарии
                    for orig_user, publications in prev_publ_dict.items():
                        for publication in publications:
                            if publication['forum_name'] == forum_name:
                                if publication['text'] == text and publication['time'] == time and publication['likes'] == likes:
                                    self.publication_list.delete(index, index + len(publication['comments']))

                                    publication['comments'].append(comment_text)

                                    self.publication_list.insert(index,f"[{publication['time']}] {user}: {publication['text']} (Likes: {publication['likes']})")
                                    # Отображаем комментарии
                                    for comment in publication['comments']:
                                        index += 1
                                        self.publication_list.insert(index, f'    Comment: {comment}')
                                        # Сохраняем обновленные данные
                                    self.save_publications(prev_publ_dict)
                                    return
                # Увеличиваем счетчик строк, добавляем одну строку за публикацию и столько строк, сколько комментариев
                real_index += (1 + len(comments))

    #   Инициализация пользовательского интерфейса
    #   Инициализация окна регистрации/входа
    def auth_init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.resizable(False, False)
        self.root.title('Messenger')
        self.root.geometry('400x300')
        self.root['bg'] = '#7dd5d2'

        Label(text='Login:', font='Sylfaen', background='#7dd5d2').place(x=30, y=35)
        Label(text='Password:', font='Sylfaen', background='#7dd5d2').place(x=30, y=115)

        # Поля для ввода логина и пароля
        self.login_entry = Entry(justify=LEFT, font='Sylfaen 12')
        self.login_entry.place(height=40, width=150, x=30, y=70)
        self.login_entry.focus()

        self.pass_entry = Entry(justify=LEFT, font='Sylfaen 12')
        self.pass_entry.place(height=40, width=150, x=30, y=150)

        # Кнопки входа и регистрации
        Button(text='Sign in', font='Sylfaen', background='White',
               command=lambda: self.sign_in(self.login_entry, self.pass_entry, self)).place(height=30, width=90, x=210, y=90)
        Button(text='Sign up', font='Sylfaen 12', background='White',
               command=lambda: self.sign_up(self.login_entry, self.pass_entry)).place(height=25, width=80, x=215, y=140)

    #   Инициализация страницы с выбором форума
    def main_page_init_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.geometry('200x300')
        self.root.title('Forums')
        self.root['bg'] = '#7dd5d2'

        #   Создаем фрейм для добавления кнопок-форумов
        self.forum_list = Frame(self.root, background='#7dd5d2', height=100, width=450)
        self.forum_list.pack(pady=20, padx=20)

        f1 = Button(self.forum_list, text='Forum 1', command=lambda: self.forum_page_init_ui('Forum 1'))
        f1.pack(pady=5)
        f2 = Button(self.forum_list, text='Forum 2', command=lambda: self.forum_page_init_ui('Forum 2'))
        f2.pack(pady=5)
        f3 = Button(self.forum_list, text='Forum 3', command=lambda: self.forum_page_init_ui('Forum 3'))
        f3.pack(pady=5)
        f4 = Button(self.forum_list, text='Forum 4', command=lambda: self.forum_page_init_ui('Forum 4'))
        f4.pack(pady=5)

        #   Кнопка выхода в окно авторизации
        logout_button = Button(self.root, text='Logout', command=self.auth_init_ui)
        logout_button.pack(pady=10)

    #   Инициализация страницы с форумом
    def forum_page_init_ui(self, forum_name):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.geometry('700x650')
        self.root.title(forum_name)
        self.root['bg'] = '#7dd5d2'

        # Фрейм для Listbox и скроллбара
        frame = Frame(self.root)
        frame.pack(pady=20, padx=20)

        self.publication_list = Listbox(frame, font='Sylfaen', height=10, width=400)
        self.publication_list.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(frame, orient=VERTICAL)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Привязываем скроллбар к Listbox
        self.publication_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.publication_list.yview)

        #   Загружаем сохранённые публикации
        if os.path.exists('published.txt'):
            try:
                with open('published.txt', 'r') as published_file:
                    content = published_file.read().strip()
                    if content != '':
                        prev_publ_dict = json.loads(content)
                        empty_flag = 1
                    else:
                        empty_flag = 0
            except (json.JSONDecodeError, FileNotFoundError):
                prev_publ_dict = {}

        #   В списке сохраним публикации в виде кортежей, отсортируем список по времени публикации
        prev_publ_tuples = []
        if empty_flag:
            for user, publications in prev_publ_dict.items():
                for publication in publications:
                    if forum_name == publication['forum_name']:
                        prev_publ_tuples.append((
                            user, publication['text'], publication['forum_name'],
                            publication['time'], publication['likes'], publication['comments']
                        ))
        prev_publ = sorted(prev_publ_tuples, key=lambda x: x[3])

        #   Добавляем старые публикации в Listbox
        for user, publication, publication_forum_name, publication_time, likes, comments in prev_publ:
            if forum_name == publication_forum_name:
                self.publication_list.insert(END, f'[{publication_time}] {user}: {publication} (Likes: {likes})')
                for comment in comments:
                    self.publication_list.insert(END, f'    Comment: {comment}')

        #   Поле ввода для добавления публикации
        self.entry = Entry(self.root)
        self.entry.pack(pady=10)
        self.entry.focus()

        #   Кнопка добавления публикации
        self.enter_button = Button(self.root, text='Enter', command=lambda: (self.save_publication(self.entry.get(), forum_name), self.entry.delete(first=0, last=END)))
        self.enter_button.pack(pady=0, padx=20)

        # Поле для добавления комментария
        self.comment_entry = Entry(self.root)
        self.comment_entry.pack(pady=10)

        # Кнопка для добавления комментария к выбранной публикации
        self.comment_button = Button(self.root, text='Add Comment', command=lambda: (self.add_comment(self.comment_entry.get(), forum_name), self.comment_entry.delete(first=0, last=END), self.entry.focus()))
        self.comment_button.pack(pady=5)

        # Кнопка для лайков
        self.like_button = Button(self.root, text='Like', command=lambda: self.like_post(forum_name))
        self.like_button.pack(pady=5)

        #   Кнопка возвращения в окно с выбором форума
        self.back_button = Button(self.root, text='Back', command=self.main_page_init_ui)
        self.back_button.pack(pady=10)

        #   Кнопка выхода в окно авторизации
        self.logout_button = Button(self.root, text='Logout', command=self.auth_init_ui)
        self.logout_button.pack(pady=10)


if __name__ == "__main__":
    root = Tk()
    app = Authorization(root)
    root.mainloop()