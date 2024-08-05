import badger2040
import jpegdec
import os
from badger2040 import WIDTH
import urequests
import json

from service.brewfather import get_batch_info, get_batches

print("Initializing beer.py")

TEXT_SIZE = 1
LINE_HEIGHT = 15

display = badger2040.Badger2040()
# Clear to white
display.set_pen(15)
display.clear()

jpeg = jpegdec.JPEG(display.display)


# 15 = White
# 0 = Black

SCREEN_SIZE = 296
LEFT_PANE = 80
PADDING = 10
RIGHT_PANE = SCREEN_SIZE - PADDING - LEFT_PANE

RIGHT_PANE_START = LEFT_PANE + PADDING

# Screen = 296x128

def display_beer_info(beer):
    print("Peparing to display beer ")
    print(beer)

    display.set_font("bitmap8")
    display.set_pen(0)
    display.rectangle(48, 0, WIDTH, 32)

    icon = "/apps/icon-beer.jpg"
    jpeg.open_file(icon)
    jpeg.decode(0, 0)

    display.set_pen(15)
    beer_label = beer.get("name", "Unnamed beer")

    title_x_offset = 52
    display.text(beer_label, title_x_offset, 8, WIDTH, TEXT_SIZE * 2)

    display.set_pen(0)

    content_x_offset = 60
    current_y = 40

    display.set_font("bitmap6")

    display.text(beer.get("style", "No Style"), content_x_offset, current_y, WIDTH, TEXT_SIZE * 2)
    current_y += LINE_HEIGHT

    display.text(str(beer.get("abv", 0)) + "%", content_x_offset, current_y, WIDTH, TEXT_SIZE * 2)
    current_y += LINE_HEIGHT

    display.text(str(beer.get("ibu", 0)) + "IBU", content_x_offset, current_y, WIDTH, TEXT_SIZE * 2)
    current_y += LINE_HEIGHT * 2


    display.set_font("bitmap8")
    display.set_thickness(4)

    display.text(", ".join(beer.get("hops", [])), content_x_offset, current_y, WIDTH - content_x_offset, TEXT_SIZE)
    current_y += LINE_HEIGHT

    display.text(beer.get("brewer", ""), content_x_offset, current_y, WIDTH - content_x_offset, TEXT_SIZE)
    current_y += LINE_HEIGHT

    display.update()

    print("[beer.py]: Display updated")


beer = get_batch_info("z6G844ONYxUVUg2s4PJpUpMh8Tv4Xb")

display_beer_info(beer)
# Call halt in a loop, on battery this switches off power.
# On USB, the app will exit when A+C is pressed because the launcher picks that up.
while True:
    display.keepalive()
    display.halt()

