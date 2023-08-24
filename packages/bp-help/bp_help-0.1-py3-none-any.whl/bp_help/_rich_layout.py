from rich import print
from rich.layout import Layout
from rich.padding import Padding
from rich.panel import Panel
from rich.prompt import Prompt
from rich.align import Align
from rich.live import Live


from rich.console import Console

from art import text2art
from time import sleep

# console = Console()

# print(console.size)

layout = Layout()

layout.split_column(
    Layout(name="upper"),
    Layout(name="lower")
)
layout["lower"].size = None
layout["lower"].ratio = 3
layout["lower"].split_row(
    Layout(name="left"),
    Layout(name="right"),
)
layout["left"].size = None
layout["left"].ratio = 2
layout["right"].split_column(
    Layout(name="upperright"),
    Layout(name="restright")
)
layout["restright"].size = None
layout["restright"].ratio = 3
layout["restright"].split_column(
    Layout(name="midright"),
    Layout(name="lowerright")
)
layout["lowerright"].size = None
layout["lowerright"].ratio = 2

text = text2art("STEPS OF DOOM", font="tarty3")
layout["upper"].update(
     Align(f'[red]{text}', align='center', vertical='middle')
)
layout["upperright"].update(
    Panel(Align(f'[bold]121.212.111', align='center', vertical='middle'), title="Your running score", 
        #   style='green'
          )
)

layout["midright"].update(
    Panel(Align(f'Time', align='center', vertical='middle'), 
            title="Recent points earned", 
            #   style='blue'
            )
)

layout["lowerright"].update(
    Panel("Hello, World!", 
          title="Recent points earned", 
        #   style='blue'
          )
)
layout["left"].update(
    Padding(Panel("\n1. Hello World\n2. Hello World", title="[red]The below steps are not in the right order!", 
                #    style='bright_black'
                  ))
)

print(layout)
sleep(1)
answer = Prompt.ask("[red]Enter line number of line to move")
layout["left"].update(
    Padding(Panel("\n1. Hello World\n[red]2. Hello World", title="[red]Ok, these are steps with that line removed:", 
                #    style='bright_black'
                  ))
)

print(layout)
answer = Prompt.ask("[red]Enter line number of line to move")
sleep(1)
print(layout)
#sleep(1)


layout["left"].update(
    Panel("\n[red]1. Hello Hello World[/red]\n2. Hello World\n3. Hello World", title="[red]Ok, these are steps with that line removed:", 
                  )
)
print(layout)
sleep(0.3)
layout["left"].update(
    Panel("\n2. Hello World\n[red]1. Hello Hello World[/red]\n3. Hello World", title="[red]Ok, these are steps with that line removed:", 
                  )
)
print(layout)
sleep(0.3)
layout["left"].update(
    Panel("\n2. Hello World\n3. Hello World\n[red]1. Hello Hello World[/red]", title="[red]Ok, these are steps with that line removed:", 
                  )
)
print(layout)
