from dataclasses import dataclass
import curses

from punkeditor.command import PunkEditorCommand


@dataclass
class KeyCommand(PunkEditorCommand):

    name = 'key'

    def loop(self, window: curses.window):
        ch = None
        while True:
            window.clear()
            if ch:
                window.addstr(hex(ch) + '\n')
            window.refresh()
            ch = window.getch()

    def execute(self):
        curses.wrapper(self.loop)
        return self.result
