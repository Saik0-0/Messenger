import json
import os.path


class Publication:
    def __init__(self, username, text):
        self.username = username
        self.text = text

    def open_data(self):
        if os.path.exists('published.txt'):
            try:
                with open('published.txt', 'r') as published_file:
                    return json.load(published_file)
            except json.JSONDecodeError:
                return {}
        return {}

    def save_data(self):
        curr_publ = self.open_data()
        if self.username in curr_publ.keys():
            curr_publ[self.username].append(self.text)
        else:
            curr_publ.setdefault(self.username, [self.text])
        with open('published.txt', 'w') as published_file:
            json.dump(curr_publ, published_file)
