
import re
import time
import random
import os
import sys
import pickle
import datetime
import cloudpickle as cp
from urllib.request import urlopen
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

from .expressions import get_expression


from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static
from textual.screen import Screen
from textual import events
from textual.widgets import RichLog, DataTable

from rich.align import Align
from rich.text import Text
from rich.style import Style as RichStyle

from art import text2art

from pygments import highlight
from pygments.style import Style
from pygments.token import Token
from pygments.lexers import Python3Lexer
from pygments.formatters import Terminal256Formatter, BBCodeFormatter, HtmlFormatter

class MyStyle(Style):
        styles = {
            Token.String:     'ansigreen',
            Token.Number:     'ansiblue',
            Token.Keyword: 'ansired',
            Token.Literal: 'ansiyellow',
            Token.Operator: 'ansibrightblue',
            Token.Text: 'ansibrightred',
            Token.Token: 'ansibrightcyan',
            Token.Name: 'ansigray',
            Token.Other: 'ansicyan',
            Token.Generic: 'ansiblack'
        }

def highlight_code(code):

    code = """ "Hello World" * 4 + len('sdf') == None"""

    s = highlight(code, Python3Lexer(), BBCodeFormatter(style=MyStyle))
    color = '#ffffff'
    s = re.sub(fr'\[color={color}\](\s+?)\[/color\]', r'\1', s)
    for color, repl in [('#007f00', 'red3'), ('#0000ff', 'black'), ('#7f0000', 'dark_magenta'), ('#00007f', 'dark_goldenrod')]:
        s = re.sub(fr'color={color}(\].*?\[/)color', fr'{repl}\1{repl}', s)
    return s

def sparkline_bars(data):
    BARS = u'▁▂▃▄▅▆▇█'
    import sys
    # data = [1, 2, 3, 4, 5, 6, 7]
    data = [float(x) for x in data if x]
    data = [(len(BARS)-1)*n/max(data) for n in data]
    incr = min(data)
    width = (max(data) - min(data)) / (len(BARS) - 1)
    bins = [i*width+incr for i in range(len(BARS))]
    indexes = []
    for n in data:
        for i, thres in enumerate(bins):
            if thres <= n < thres+width:
                indexes.append(i)
                break
    sparkline = ''.join(BARS[i] for i in indexes)

class KeyLogger(RichLog):

    def __init__(self, markup=True):
        super().__init__(markup=markup)

    def on_mount(self):
        self.next_expression()

    def on_key(self, event: events.Key):
        self.clear()
        if event.key.isdigit():
            line_num = int(event.key)
            self.write(f'highlight line {line_num}')            

    def key_up(self):
        self.clear()
        s = highlight(""" "Hello World" * 4 + len('sdf') == None""", Python3Lexer(), BBCodeFormatter(style=MyStyle))
        s = highlight_code(s)
        self.write(s)
        self.write('arrow up')

    def key_down(self):
        self.clear()
        self.write('arrow down')

    def next_expression(self):
        self.clear()
        steps = ['step + one', 'step + two', 'step + three']
        
        self.write('\n'.join(steps))



from itertools import cycle
hellos = cycle(
    [
        "Hola",
        "Bonjour",
        "Guten tag",
        "Salve",
        "Nǐn hǎo",
        "Olá",
        "Asalaam alaikum",
        "Konnichiwa",
        "Anyoung haseyo",
        "Zdravstvuyte",
        "Hello",
    ]
)




#https://www.i2symbol.com/symbols/smileys


ROWS = [
    ("Week", "Days", "Steak", "Score"),
    (1,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 111221150),
    (2,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 51.14),
    (3,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★  |", 51.14),
    (4,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|[bright_red]★★★★★★★[/bright_red]|🏆", 51.14),
    (5,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 51.58),
    (6,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 51.73),
    (7,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 50.39),
    (8,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 50.39),
    (9,  sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 51.14),
    (10, sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★  |", 51.14),
    (11, sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★ |", 51.14),
    (12, sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★    |", 51.26),
    (13, sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 51.58),
    (14, sparkline_bars([1, 2, 3, 4, 5, 6, 7]), u"|★★★★★★★|", 51.73),
]


class PlayerStats(DataTable):

    def on_mount(self) -> None:
#        table = self.query_one(PlayerStats)
        header_style = RichStyle(color='bright_white', bold=False, blink=True)
        styled_header = [
            Text(str(cell), style=header_style, justify='left') for cell in ROWS[0]
        ]
        self.add_columns(*styled_header)
        # self.add_columns(*ROWS[0])
        self.add_rows(ROWS[1:])
        self.show_cursor = False
        self.zebra_stripes = True


# TODO: welcome screen with pep talk and status for reaching score goal, 
# appreaciation for getting back to the program if it has been a while
# encouragement, personal comments based on past streaks (you can do it again)


class STEPS(Screen):
    BINDINGS = [("h", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
#        yield Header()
        with Container(id="header"):
            text = text2art("STEP-TRAINER", font="tarty3")
            head = Align(f'{text}', align='center', vertical='middle')
            yield Static(head)
        with Container(id="app-grid"):
            with Vertical(id="left-pane"):
                # yield Header()
                yield KeyLogger()
            with Horizontal(id="top-right"):
                # yield Header(show_clock=True)
                yield PlayerStats()
            with Horizontal(id="bottom-right"):
                # yield Header()
                s = """This week's score gloal: 1002012211
You still need to earn:  1002012211"""
                s = Text(s, style=RichStyle(color='bright_red', bgcolor='yellow', italic=True, bold=True, blink=True), justify='left')
                yield Static(s)

class STEPSApp(App):
    CSS_PATH = "text_gui.css"
    dark = False
    SCREENS = {"steps": STEPS()}
    BINDINGS = [("escape", "push_screen('steps')", "STEPS")]

    def on_mount(self) -> None:
        self.push_screen(STEPS())

def run():
    app = STEPSApp()
    app.run()


if __name__ == "__main__":
    app = STEPSApp()
    app.run()
