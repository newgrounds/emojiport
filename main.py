from kivy.app import App
from kivy.uix.widget import Widget

class EmojiportUI(Widget):
    pass

class EmojiportApp(App):
    def build(self):
        return EmojiportUI()

if __name__ == '__main__':
    EmojiportApp().run()