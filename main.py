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
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty

from bookcollection import BookCollection
from book import Book


# Constants for work with files
FILENAME = 'books.csv'


class MainScreen(Screen):
    """Base screen."""
    def __init__(self, books=None, **kwargs):
        super().__init__(**kwargs)
        self.books = books
        self.main_box = None

    def on_enter(self):
        # Базовый бокс
        self.main_box = MainBox(self.books)
        self.add_widget(self.main_box)


class BookButton(Button):
    """Кнопка со ссылкой на определенную книгу."""
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
        """Установка цвета кнопки в зависимости от необходимости/завершения чтения"""
        self.background_color = 'white' if self.book.is_completed else 'aqua'

    def on_press(self):
        """Обработка нажатия на кнопку книги"""
        if self.book.is_completed:
            self.book.mark_required()
        else:
            self.book.mark_completed()
        self.set_color()
        self.text = str(self.book)
        self.top_label.set_label_text()
        text = '{} \'{}\'.{}'.format(
            'Вы прочитали' if self.book.is_completed else 'Вам нужно прочитать',
            self.book.title,
            (' Хорошая работа!' if self.book.is_completed else ' Начнем!') if self.book.is_long() else ''
        )
        self.warn_label.set_label_text(text)


class BookLabel(Label):
    """Базовый класс надписей"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        return self


class HeadLabel(BookLabel):
    """Верхняя надпись."""
    def __init__(self, collection=None, **kwargs):
        super().__init__(**kwargs)
        self.collection = collection

    def set_label_text(self):
        """Выводит количество страниц, требуемых для прочтения"""
        self.text = 'Необходимо прочитать: {} стр.'.format(self.collection.get_required_pages())

    # def test(self):
    #     return self.collection.get_required_pages()


class WarningLabel(BookLabel):
    """Нижняя информационная надпись"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_label_text("Добро пожаловать в Reading Tracker 2.0!")
        self.warn = False

    def set_label_text(self, text, warn=False):
        """Устанавливает текст и цвет надписи"""
        self.text = text
        self.warn = warn
        self.opacity = .8
        if self.warn:
            self.color = 'darksalmon'
        else:
            self.color = 'lightgreen'
        self.on_size()

    def on_size(self, *args):
        """Устанавливает цвет фона надписи"""
        self.canvas.before.clear()
        if hasattr(self, 'warn'):
            color = (.8, 0, 0) if self.warn else (0, .5, 0)
        else:
            color = (0, .5, 0)
        with self.canvas.before:
            Color(*color, 0.25)
            Rectangle(pos=self.pos, size=self.size)


class MainBox(BoxLayout):
    """Базовый класс макета страницы"""
    # Ссылки на части макета страницы, которые установлены в kv-файле
    spinner = ObjectProperty(None)
    maingrid = ObjectProperty(None)
    recycle = ObjectProperty(None)
    headlabel = ObjectProperty(None)
    warnlabel = ObjectProperty(None)

    def __init__(self, books=None, **kwargs):
        super().__init__(**kwargs)
        self.books = books
        self.init_grid()
        # Маркеры определения внутреннего названия объекта
        self.ids_obj = dict(zip(self.ids.values(), self.ids.keys()))
        # Маркеры перехода по объектам TextInput при нажатии tab
        self.markers = [self.ids['add_title'], self.ids['add_author'], self.ids['add_pages']]

    def init_grid(self):
        """Предварительные действия при инициализации страницы"""
        self.headlabel.collection = self.books
        self.headlabel.set_label_text()
        self.warnlabel.set_label_text("Добро пожаловать в Reading Tracker 2.0!")
        self.building_grid(None, 'Автору')

    def building_grid(self, instance, value):
        """Построение списка книг"""
        LABEL_MAP = {
            'Автору': 'author',
            'Названию': 'title',
            'Страницам': 'pages',
            'Прочитано': 'completed',
        }
        # self.books.sort(value)
        self.books.sort(LABEL_MAP[value])
        # Построение окна прокрутки
        self.recycle.width = Window.width
        self.recycle.height = Window.height - self.headlabel.height - self.warnlabel.height
        self.maingrid.bind(
            minimum_height=self.maingrid.setter('height')
        )
        # Перерисовка списка книг
        self.maingrid.clear_widgets()
        for book in self.books:
            self.maingrid.add_widget(
                BookButton(
                    book=book,
                    top_label=self.headlabel,
                    warn_label=self.warnlabel,
                    text=str(book),
                    size_hint_y=None
                )
            )

    def add_book(self, title_obj, author_obj, pages_obj):
        """Обработка добавления книги"""
        title, author, pages = map(str.strip, (title_obj.text, author_obj.text, pages_obj.text))
        # Проверка правильности ввода полей
        if not title or not author or not pages:
            self.warnlabel.set_label_text('Все поля должны быть заполнены!', True)
            return
        try:
            pages = int(pages)
        except ValueError:
            self.warnlabel.set_label_text('Пожалуйста, введите корректное число!', True)
            return
        if pages < 1:
            self.warnlabel.set_label_text('Число страниц должно быть больше 0!', True)
            return
        self.warnlabel.set_label_text('Вы добавили новую книгу')
        self.books.add_book(Book(title=title, author=author, number_of_pages=pages))
        self.headlabel.set_label_text()
        self.building_grid(None, self.spinner.text)
        self.clear_addfields(title_obj, author_obj, pages_obj)

    def clear_addfields(self, title, author, pages):
        """Очистка полей добавления книги"""
        title.text = ''
        author.text = ''
        pages.text = ''

    def text_control(self, field):
        """Контроллирование перемещения по полям ввода tab'ом"""
        if field.text.endswith('\t'):
            field.text = field.text[:-1]
            idx = self.markers.index(field)
            field.focus = False
            if idx == len(self.markers)-1:
                self.markers[0].focus = True
            else:
                self.markers[idx+1].focus = True


class ReadingTrackerApp(App):
    """Базовое приложение"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.books = BookCollection()
        try:
            self.books.load_books()
        except (FileNotFoundError, LookupError):
            pass

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(self.books))
        return sm

    def on_stop(self):
        """Сохранение обновленного файла со списком книг"""
        self.books.save_books()
        return super().on_stop()


if __name__ == '__main__':
    ReadingTrackerApp().run()
