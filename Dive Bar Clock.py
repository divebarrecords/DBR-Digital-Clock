import os
import sys
from time import strftime
from tkinter import Tk, Canvas
from PIL import ImageTk, Image, ImageDraw, ImageFont

BG = "#2d443e"
FG = "#D79922"
WIDTH, HEIGHT = 200, 80
FONT_SIZE = 40


def resource_path(name):
    """Find a bundled file whether running as a script or a PyInstaller app."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)


window = Tk()
window.title("Dive Bar Clock")
window.geometry(f"{WIDTH}x{HEIGHT}")
window.configure(bg=BG)
window.resizable(False, False)

canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg=BG, highlightthickness=0, bd=0)
canvas.pack()

# Background bottle
bottle = Image.open(resource_path("BOTTLE.png")).convert("RGBA")
scale = (HEIGHT - 10) / bottle.height
bottle = bottle.resize((int(bottle.width * scale), HEIGHT - 10), Image.LANCZOS)
bottle_img = ImageTk.PhotoImage(bottle)
canvas.create_image(5, HEIGHT // 2, image=bottle_img, anchor="w")

# Clock text, rendered with Pillow using the bundled font
font = ImageFont.truetype(resource_path("Freya.ttf"), FONT_SIZE)
text_item = canvas.create_image(WIDTH - 10, HEIGHT // 2, anchor="e")
text_photo = None  # keep a reference so it isn't shite collected


def update_label():
    global text_photo
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.multiline_text(
        (WIDTH - 10, HEIGHT // 2),
        strftime("%H:%M:%S\n%d-%m-%Y"),
        font=font, fill=FG, anchor="rm", align="right",
    )
    text_photo = ImageTk.PhotoImage(layer)
    canvas.itemconfigure(text_item, image=text_photo)
    canvas.coords(text_item, WIDTH, HEIGHT // 2)
    window.after(1000, update_label)


update_label()
window.mainloop()