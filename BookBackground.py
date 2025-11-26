from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Button, Static
from textual.screen import Screen

class MainPage(Screen):

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Static("", id="spine"),

                Container(
                    Static("[center]Project42[/center]", id="title"),
                    Container(
                        Button("Login", id="login", classes="menu-btn"),
                        Button("Registreer", id="register", classes="menu-btn"),
                        id="button-area"
                    ),
                    id="left", classes="page",
                ),

                Static("[center]Welkom![/center]", id="right", classes="page"),
                id="book"
            ),
            id="book-wrapper"
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "login":
            print("Login clicked")  # Placeholder
        elif event.button.id == "register":
            print("Register clicked")  # Placeholder


class BookApp(App):
    CSS_PATH = "styles.tcss"

    def on_mount(self):
        self.push_screen(MainPage())


if __name__ == "__main__":
    BookApp().run()
