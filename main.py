"""
Name:
Date:
Brief Project Description:
GitHub URL:
"""
# Create your main program in this file, using the ReadingTrackerApp class

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.metrics import dp

from bookcollection import BookCollection


# Constants for work with files
FILENAME = 'books.csv'

class MainScreen(Screen):
    
    def __init__(self, books=None, **kwargs):
        super().__init__(**kwargs)
        self.books = books

    def on_enter(self):
        # Базовый бокс
        self.main_layout = BoxLayout()
        self.add_widget(self.main_layout)

        sort_label = Label(
            text='Sort by:',
            size_hint_x=1,
            font_size=20,
        )
        self.main_layout.add_widget(sort_label)

        right_box = BoxLayout(
            orientation='vertical',
            size_hint_x=3
        )
        self.main_layout.add_widget(right_box)

        self.layout = GridLayout(
            cols=1,
            spacing=10,
            size_hint_y=None
        )
        self.layout.bind(
            minimum_height=self.layout.setter('height')
        )

        title_label = Label(
            text='Test program label',
            size_hint_y=None,
            height=dp(40),
            font_size=16
        )
        right_box.add_widget(title_label)

        root = RecycleView(
            size_hint=(1, None),
            width=Window.width,
            # height=Window.height-title_label.height
        )
        root.add_widget(self.layout)
        right_box.add_widget(root)

        warn_label = Label(
            text='Warning test label',
            size_hint_y=None,
            height=dp(50),
            color='red',
            font_size=16
        )
        right_box.add_widget(warn_label)
        root.height = Window.height-title_label.height-warn_label.height

        for book in self.books:
            self.layout.add_widget(BookButton(book))

class BookButton(Button):

    def __init__(self, book, **kwargs):
        super().__init__(**kwargs)
        self.book = book
        self.set_color()
        self.text = str(book)

    def build(self):
        return self

    def set_color(self):
        self.background_color = 'white' if self.book.is_completed else 'aqua'


class ReadingTrackerApp(App):
    """..."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.books = BookCollection()
        try:
            # WARNING пока без сохранения backup
            self.books.load_books(FILENAME, backup=False)
        except (FileNotFoundError, LookupError):
            pass

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(self.books))
        return sm


if __name__ == '__main__':
    ReadingTrackerApp().run()
