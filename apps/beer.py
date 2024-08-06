import badger2040
import jpegdec
from badger2040 import WIDTH
from apps.actions import Actions
from badger_util import clear_screen, wait_for_user_to_release_buttons
from service.brewfather import get_batch_info

LINE_HEIGHT = 15

display = badger2040.Badger2040()
clear_screen(display)

jpeg = jpegdec.JPEG(display.display)

SCREEN_SIZE = 296
LEFT_PANE = 80
PADDING = 10
RIGHT_PANE = SCREEN_SIZE - PADDING - LEFT_PANE

RIGHT_PANE_START = LEFT_PANE + PADDING

# Screen = 296x128

class BeerDisplay:

    def __init__(self, manager):
        self.manager = manager

    def show_beer(self, beer_id):
        beer = get_batch_info(beer_id)
        return self.display_beer_info(beer)

    def display_beer_info(self, beer):
        clear_screen(display)

        display.set_font("bitmap8")
        display.set_pen(0)
        display.rectangle(48, 0, WIDTH, 32)

        icon = "/apps/icon-beer.jpg"
        jpeg.open_file(icon)
        jpeg.decode(0, 0)

        display.set_pen(15)
        title_x_offset = 52

        beer_label = beer.get("name", "Unnamed beer")
        beer_label_size = display.measure_text(beer_label, 2)
        title_holder_size = WIDTH - title_x_offset

        label_scale = 2 if beer_label_size < title_holder_size else 1

        display.text(beer_label, title_x_offset, 8, title_holder_size - 5, label_scale)

        display.set_pen(0)

        content_x_offset = 60
        current_y = 40

        display.set_font("bitmap6")

        beer_big_info = beer.get("style", "No Style") + "\n" \
        + str(beer.get("abv", 0)) + "%\n" \
        + str(beer.get("ibu", 0)) + "IBU"

        display.text(beer_big_info, content_x_offset, current_y, WIDTH, 2)

        current_y += LINE_HEIGHT * 4

        display.set_font("bitmap8")
        display.set_thickness(4)

        display.text(", ".join(beer.get("hops", [])), content_x_offset, current_y, WIDTH - content_x_offset, 1)
        current_y += LINE_HEIGHT

        display.text(beer.get("brewer", ""), content_x_offset, current_y, WIDTH - content_x_offset, 1)
        current_y += LINE_HEIGHT

        display.set_update_speed(badger2040.UPDATE_NORMAL)
        display.update()
        display.set_update_speed(badger2040.UPDATE_FAST)


        while True:
            # Sometimes a button press or hold will keep the system
            # powered *through* HALT, so latch the power back on.
            display.keepalive()

            if display.pressed_any():
                print("Something pressed")
                wait_for_user_to_release_buttons(display)
                break

            display.halt()

        return Actions.GO_TO_LISTING
