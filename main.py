from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

MOTEURS = {
    "Google":     "https://www.google.com/search?q=",
    "DuckDuckGo": "https://duckduckgo.com/?q=",
    "Qwant":      "https://www.qwant.com/?q=",
}
MOTEUR_ACTUEL = "Google"
VERT  = get_color_from_hex("#00853F")
JAUNE = get_color_from_hex("#FDEF42")
ROUGE = get_color_from_hex("#E31B23")
NOIR  = get_color_from_hex("#1a1a1a")
BLANC = get_color_from_hex("#FFFFFF")

class XoolalApp(App):
    def build(self):
        Window.clearcolor = NOIR
        self.title = "Xoolal"
        layout = BoxLayout(orientation='vertical')
        barre = BoxLayout(size_hint_y=None, height=60, spacing=5, padding=5)
        btn_retour = Button(text="<", size_hint_x=None, width=50, background_color=VERT)
        barre.add_widget(btn_retour)
        self.url_bar = TextInput(
            hint_text="Rechercher ou URL...",
            multiline=False, background_color=BLANC, foreground_color=NOIR)
        self.url_bar.bind(on_text_validate=self.naviguer)
        barre.add_widget(self.url_bar)
        btn_go = Button(text=">", size_hint_x=None, width=50, background_color=ROUGE)
        btn_go.bind(on_press=self.naviguer)
        barre.add_widget(btn_go)
        layout.add_widget(barre)
        label = Label(
            text="Xoolal Browser - Ismaila Mbodji",
            size_hint_y=None, height=30, font_size=12, color=JAUNE)
        layout.add_widget(label)
        return layout

    def naviguer(self, instance=None):
        texte = self.url_bar.text.strip()
        if not texte:
            return

if __name__ == "__main__":
    XoolalApp().run()
