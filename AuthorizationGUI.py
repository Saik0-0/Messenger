from tkinter import *

from Authorization import Authorization


class Messenger:
    def __init__(self, root):
        self.root = root
        self.auth_init_ui()
        self.auth = Authorization()

    # Инициализация пользовательского интерфейса
    def auth_init_ui(self):
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
        Button(text='Sign in', font='Sylfaen', background='White', command=lambda: self.auth.sign_in(self.login_entry, self.pass_entry, self)).place(height=30, width=90, x=210, y=260)
        Button(text='Sign up', font='Sylfaen 12', background='White', command=lambda: self.auth.sign_up(self.login_entry, self.pass_entry)).place(height=25, width=80, x=215, y=310)

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
    app = Messenger(root)
    root.mainloop()
