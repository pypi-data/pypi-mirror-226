from pathlib import Path

from textual.app import App, ComposeResult
from textual.keys import Keys
from textual.widgets import Header, Footer, DirectoryTree


class ThinkingTree(DirectoryTree):
    pass


class ThinkingFace(App):
    """ThinkingFace App"""

    TITLE: str = "Thinking Face 🤔"

    def compose(self) -> ComposeResult:
        yield Header()
        directory = Path.cwd()
        tree = ThinkingTree("./")
        yield tree
        yield Footer()


def main():
    app = ThinkingFace()
    app.run()
