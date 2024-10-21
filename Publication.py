import json
import os.path


class Publication:
    def __init__(self, username, text, forum_name, time, likes=0, comments=None):
        self.username = username
        self.text = text
        self.forum_name = forum_name
        self.time = time
        self.likes = likes
        if comments is None:
            comments = []
        self.comments = comments

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
            curr_publ[self.username].append({
                'text': self.text,
                'forum_name': self.forum_name,
                'time': self.time,
                'likes': self.likes,
                'comments': self.comments
            })
        else:
            curr_publ.setdefault(self.username, [{
                'text': self.text,
                'forum_name': self.forum_name,
                'time': self.time,
                'likes': self.likes,
                'comments': self.comments
            }])
        with open('published.txt', 'w') as published_file:
            json.dump(curr_publ, published_file)
