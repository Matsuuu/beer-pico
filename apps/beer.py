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
display.led(128)

jpeg = jpegdec.JPEG(display.display)

# Clear to white
display.set_pen(15)
display.clear()

# 15 = White
# 0 = Black

SCREEN_SIZE = 296
LEFT_PANE = 80
PADDING = 10
RIGHT_PANE = SCREEN_SIZE - PADDING - LEFT_PANE

RIGHT_PANE_START = LEFT_PANE + PADDING

beer = get_batch_info("z6G844ONYxUVUg2s4PJpUpMh8Tv4Xb")
print("BEER ")
print(beer)

# Screen = 296x128

def display_beer_info(beer):
    display.set_font("bitmap8")
    display.set_pen(0)
    display.rectangle(48, 0, WIDTH, 32)

    icon = "/apps/icon-beer.jpg"
    jpeg.open_file(icon)
    jpeg.decode(0, 0)

    display.set_pen(15)
    beer_label = "System Shock"

    title_x_offset = 52
    display.text(beer_label, title_x_offset, 8, WIDTH, TEXT_SIZE * 2)

    display.set_pen(0)

    content_x_offset = 60
    current_y = 40

    display.set_font("bitmap6")

    display.text("West Coast IPA", content_x_offset, current_y, WIDTH, TEXT_SIZE * 2)
    current_y += LINE_HEIGHT

    display.text("7.1% abv.", content_x_offset, current_y, WIDTH, TEXT_SIZE * 2)
    current_y += LINE_HEIGHT

    display.text("60 IBU", content_x_offset, current_y, WIDTH, TEXT_SIZE * 2)
    current_y += LINE_HEIGHT * 2


    display.set_font("bitmap8")
    display.set_thickness(4)

    display.text("Amarillo, Cascade, Simcoe, Loral", content_x_offset, current_y, WIDTH - content_x_offset, TEXT_SIZE)
    current_y += LINE_HEIGHT

    display.text("Matsu Brewing", content_x_offset, current_y, WIDTH - content_x_offset, TEXT_SIZE)
    current_y += LINE_HEIGHT

    batches = get_batches()
    print(batches['batches'][0]['brewer'])

# display.text("info", WIDTH - display.measure_text("help", 0.4) - 4, 4, WIDTH, 1)

# display.set_pen(0)

# y = 32 + int(LINE_HEIGHT / 2)

# display.text("Trying to get shit to work", 5, y, WIDTH, TEXT_SIZE)
# y += LINE_HEIGHT
# display.text("Dual-core RP2040, 133MHz, 264KB RAM", 5, y, WIDTH, TEXT_SIZE)
# y += LINE_HEIGHT
# display.text("2MB Flash (1MB OS, 1MB Storage)", 5, y, WIDTH, TEXT_SIZE)
# y += LINE_HEIGHT
# display.text("296x128 pixel Black/White e-Ink", 5, y, WIDTH, TEXT_SIZE)
# y += LINE_HEIGHT
# y += LINE_HEIGHT

# display.text("For more info:", 5, y, WIDTH, TEXT_SIZE)
# y += LINE_HEIGHT
# display.text("https://pimoroni.com/badger2040", 5, y, WIDTH, TEXT_SIZE)

display.update()

print("[beer.py]: Display updated")
# Call halt in a loop, on battery this switches off power.
# On USB, the app will exit when A+C is pressed because the launcher picks that up.
while True:
    display.keepalive()
    display.halt()

