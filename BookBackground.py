from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Static, Markdown
from textual.screen import Screen
from textual.reactive import reactive
from textual.events import Click
import asyncio

class BookViewer(Screen):
    pages = reactive(0)

    def __init__(self, page_contents: list[str]):
        super().__init__()
        self.page_contents = page_contents

    def compose(self) -> ComposeResult:
        yield Container(
            Container(
                Static("", id="spine"),  # Book spine
                self.create_page_widget(self.page_contents[self.pages], "left"),
                self.create_page_widget(self.page_contents[(self.pages + 1) % len(self.page_contents)], "right"),
                id="book"
            ),
            id="book-wrapper"
        )

    def create_page_widget(self, content: str, widget_id: str):
        """Create Static for centered title, or Markdown for normal content."""
        if content.startswith("[center]"):  # detect titles
            text = content.replace("[center]", "").replace("[/center]", "").strip()
            return Static(text, id=widget_id, classes="page centered-title")
        else:
            return Markdown(content, id=widget_id, classes="page")

    def on_mount(self) -> None:
        self.update_page()

    def update_page(self):
        # Left page
        left_content = self.page_contents[self.pages]
        left_page = self.query_one("#left")
        if isinstance(left_page, Static):
            left_page.update(left_content.replace("[center]", "").replace("[/center]", "").strip())
        else:
            left_page.update(left_content)

        # Right page
        next_page_index = (self.pages + 1) % len(self.page_contents)
        right_content = self.page_contents[next_page_index]
        right_page = self.query_one("#right")
        if isinstance(right_page, Static):
            right_page.update(right_content.replace("[center]", "").replace("[/center]", "").strip())
        else:
            right_page.update(right_content)

    async def on_click(self, event: Click) -> None:
        await self.turn_page(1)

    async def on_key(self, event):
        if event.key == "right":
            await self.turn_page(1)
        elif event.key == "left":
            await self.turn_page(-1)
        elif event.key == "q":
            await self.app.pop_screen()

    async def turn_page(self, direction: int):
        await self.animate_flip(direction)

    async def animate_flip(self, direction: int):
        book = self.query_one("#book")

        book.styles.opacity = 0.2
        book.styles.offset_x = 5 * direction
        await asyncio.sleep(0.15)

        self.pages = (self.pages + (2 * direction)) % len(self.page_contents)
        self.update_page()

        book.styles.offset_x = -3 * direction
        await asyncio.sleep(0.05)
        book.styles.opacity = 1
        book.styles.offset_x = 0


class BookApp(App):
    CSS_PATH = "styles.tcss"

    def on_mount(self):
        pages = [
            "[center]=== PROJECT 42 ===[/center]",
            "[center]Chapter I[/center]",
            "[center]Chapter II[/center]",
            "[center]Final Page[/center]"
        ]
        self.push_screen(BookViewer(pages))


if __name__ == "__main__":
    BookApp().run()
