"""
Name:
Date:
Brief Project Description:
GitHub URL:
"""
# Create your main program in this file, using the ReadingTrackerApp class

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import ObjectProperty

from bookcollection import BookCollection


# Constants for work with files
FILENAME = 'books.csv'

class MainScreen(Screen):
    
    def __init__(self, books=None, **kwargs):
        super().__init__(**kwargs)
        self.books = books

    def on_enter(self):
        # Базовый бокс
        self.main_box = MainBox(self.books)
        self.add_widget(self.main_box)
        # self.main_layout = BoxLayout()
        # self.add_widget(self.main_layout)

        # left_box = BoxLayout(
        #     orientation='vertical',
        #     size_hint_x=1
        # )
        # self.main_layout.add_widget(left_box)

        # left_box.add_widget(Label(
        #     text='Sort by:',
        #     font_size=16
        # ))

        # left_box.add_widget(SortingSpinner(self.books))

        # right_box = BoxLayout(
        #     orientation='vertical',
        #     size_hint_x=3
        # )
        # self.main_layout.add_widget(right_box)

        # self.layout = GridLayout(
        #     cols=1,
        #     spacing=10,
        #     size_hint_y=None
        # )
        # self.layout.bind(
        #     minimum_height=self.layout.setter('height')
        # )

        # self.top_label = HeadLabel(self.books)
        # right_box.add_widget(self.top_label)

        # root = RecycleView(
        #     size_hint=(1, None),
        #     width=Window.width,
        # )
        # root.add_widget(self.layout)
        # right_box.add_widget(root)

        # self.warn_label = WarningLabel()
        # right_box.add_widget(self.warn_label)
        # # warn_label.set_label_text('Warning', True)
        
        # root.height = Window.height-self.top_label.height-self.warn_label.height

        # for book in self.books:
        #     self.layout.add_widget(BookButton(book, self.top_label, self.warn_label))

# class CollectionGrid(RecycleView):

#     def __init__(self, collection, **kwargs):
#         super().__init__(**kwargs)
#         self.collection = collection

    # def get_collection(self):
    #     return self.collection

    # def 

class SortingSpinner(Spinner):

    def __init__(self, collection, **kwargs):
        super().__init__(**kwargs)
        self.collection = collection
        self.sort_collection()

    def build(self):
        return self

    def show_text(self):
        print(self.text)

    def sort_collection(self):
        self.collection.sort(self.text.lower())
        print(self.collection)

class BookButton(Button):

    def __init__(self, book, top_label, warn_label, **kwargs):
        super().__init__(**kwargs)
        self.book = book
        self.top_label = top_label
        self.warn_label = warn_label
        self.set_color()
        self.text = str(book)

    def build(self):
        return self

    def set_color(self):
        self.background_color = 'white' if self.book.is_completed else 'aqua'

    def on_press(self):
        if self.book.is_completed:
            self.book.mark_required()
        else:
            self.book.mark_completed()
        self.set_color()
        self.text = str(self.book)
        self.top_label.set_label_text()
        text = 'You {} \'{}\'.{}'.format(
            'completed' if self.book.is_completed else 'need to read',
            self.book.title,
            (' Great job!' if self.book.is_completed else ' Get started!') if self.book.is_long() else ''
        )
        self.warn_label.set_label_text(text)


class BookLabel(Label):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return self

class HeadLabel(BookLabel):

    def __init__(self, collection=None, **kwargs):
        super().__init__(**kwargs)
        self.collection = collection
        # self.set_label_text()

    def set_label_text(self):#, text=''):
        # if text:
        #     self.text = text
        # else:
        self.text = 'Pages to read: {}'.format(self.collection.get_required_pages())

    def test(self):
        return self.collection.get_required_pages()


class WarningLabel(BookLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_label_text('Welcome to the Reading Tracker 2.0!')
        self.warn = False

    def set_label_text(self, text, warn=False):
        self.text = text
        self.warn = warn
        self.opacity = .8
        if self.warn:
            self.color = 'darksalmon'
        else:
            self.color = 'lightgreen'
        self.on_size()

    def on_size(self, *args):
        self.canvas.before.clear()
        if hasattr(self, 'warn'):
            color = (.8,0,0) if self.warn else (0,.5,0)
        else:
            color = (0,.5,0)
        with self.canvas.before:
            Color(*color, 0.25)
            Rectangle(pos=self.pos, size=self.size)


class MainBox(BoxLayout):

    spinner = ObjectProperty(None)
    maingrid = ObjectProperty(None)
    recycle = ObjectProperty(None)
    headlabel = ObjectProperty(None)
    warnlabel = ObjectProperty(None)

    def __init__(self, books=None, **kwargs):
        super().__init__(**kwargs)
        self.books = books
        self.init_grid()

    def init_grid(self):
        self.headlabel.collection = self.books
        self.headlabel.set_label_text()
        self.warnlabel.set_label_text('Welcome to the Reading Tracker 2.0!')
        self.building_grid(None, 'Author')

    def building_grid(self, instance, value):
        # print('Object from event:', instance)
        # print('Value from event:', value)
        # self.headlabel.set_label_text(self.books.get_required_pages())
        # self.warnlabel.set_label_text('Welcome to the Reading Tracker 2.0!')
        self.recycle.width = Window.width
        self.recycle.height = Window.height - self.headlabel.height - self.warnlabel.height
        # Позволяет полностью прокручивать окно (иначе низ списка не до конца виден)
        self.maingrid.bind(
            minimum_height=self.maingrid.setter('height')
        )
        self.maingrid.clear_widgets()
        for book in self.books:
            # print(x, end=' ')
            self.maingrid.add_widget(
                BookButton(
                    book=book,
                    top_label=self.headlabel,
                    warn_label=self.warnlabel,
                    text=str(book),
                    size_hint_y=None
                )
            )


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
