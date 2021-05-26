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


class MainScreen(Screen):
    
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def on_enter(self):
        self.main_layout = GridLayout(
            cols=2,
            rows=1,
            spacing=10
        )
        self.add_widget(self.main_layout)
        # left_box = BoxLayout(
        #     padding=10
        #     # spacing=10
        # )
        # self.add_widget(self.main_layout)
        # right_box = BoxLayout(
        #     padding=10
        # )
        # self.add_widget(self.main_layout)

        sort_label = Label(
            text='Sort by:',
            # outline_color='#484848',
            # outline_width=3
        )
        self.main_layout.add_widget(sort_label)

        right_box = BoxLayout(
            padding=10,
            orientation='vertical',
            # size_hint_y=None
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
        # right_box.add_widget(self.layout)

        title_label = Label(
            text='Test program label',
            size_hint_y=None,
            height=dp(40)
        )
        right_box.add_widget(title_label)

        root = RecycleView(
            size_hint=(1, None),
            # size - размер виджета (свойства width и height)
            # size=(Window.width, Window.height-title_label.height)
            width=Window.width,
            height=Window.height-title_label.height
        )
        root.add_widget(self.layout)
        right_box.add_widget(root)

        warn_label = Label(
            text='Warning test label',
            size_hint_y=None,
            height=dp(50),
            color=(1, 0, 255, 1)
        )
        right_box.add_widget(warn_label)
        root.height = Window.height-title_label.height-warn_label.height

        for num in range(10):
            btn = Button(
                text=str(num)*10,
                size_hint_y=None,
                # height=dp(40)
            )
            self.layout.add_widget(btn)

class ReadingTrackerApp(App):
    """..."""
    def __init__(self):
        super().__init__()
        self.collection = BookCollection()

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        return sm


if __name__ == '__main__':
    ReadingTrackerApp().run()
