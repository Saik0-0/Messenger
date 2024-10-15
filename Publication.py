import json
import os.path


class Publication:
    def __init__(self, username, text, forum_name, time):
        self.username = username
        self.text = text
        self.forum_name = forum_name
        self.time = time

    #   Функция загрузки старых публикаций из файла
    def open_data(self):
        if os.path.exists('published.txt'):
            try:
                with open('published.txt', 'r') as published_file:
                    return json.load(published_file)
            except json.JSONDecodeError:
                return {}
        return {}

    #   Функция сохранения новой публикации
    def save_data(self):
        curr_publ = self.open_data()
        #   Проверяем, делал ли уже публикации данный пользователь
        if self.username in curr_publ.keys():
            curr_publ[self.username].append((self.text, self.forum_name, self.time))
        else:
            curr_publ.setdefault(self.username, [(self.text, self.forum_name, self.time)])
        with open('published.txt', 'w') as published_file:
            json.dump(curr_publ, published_file)
