from service.brewfather import get_batches
import badger2040
from badger2040 import HEIGHT, WIDTH

from badger_util import clear_screen


display = badger2040.Badger2040()
display.set_update_speed(badger2040.UPDATE_FAST)

# Approximate center lines for buttons A, B and C
centers = (41, 147, 253)

class BeerListing():

    batches = []
    current_page = 0
    current_selected_item = 0;
    items_per_page = 7

    def __init__(self):
        clear_screen(display)
        self.batches = get_batches(self.items_per_page)
        self.list_batches()

    def list_batches(self):
        clear_screen(display)
        y = 4
        LINE_HEIGHT = 15
        # Draw menu items
        for i, batch in enumerate(self.batches):
            if self.current_selected_item == i:
                display.set_pen(0)
                display.rectangle(2, y, WIDTH - 4, LINE_HEIGHT)
                display.set_pen(15)
                display.text(batch.get("recipe", "<No Recipe>").get("name", "<No Name>"), 4, y)
            else:
                display.set_pen(0)
                display.text(batch.get("recipe", "<No Recipe>").get("name", "<No Name>"), 4, y)
            y += LINE_HEIGHT

        # Draw instructions
        menu_items = ["", "Info", "Select"]

        display.set_pen(0)
        display.rectangle(0, HEIGHT - 10, WIDTH, 10)
        display.set_pen(15)

        for i, menu_item in enumerate(menu_items):
            text_width = display.measure_text(menu_item, 1)
            display.text(menu_item, centers[i] - round(text_width / 2), HEIGHT - 8, 300, 1)

        display.update()

    def previous_item(self):
        print("previous")
        if self.current_selected_item == 0 and self.current_page == 0:
            return
        if self.current_selected_item == 0 and self.current_page > 0:
            self.current_page -= 1

        self.current_selected_item -= 1
        display.set_update_speed(badger2040.UPDATE_TURBO)
        self.list_batches()
        display.set_update_speed(badger2040.UPDATE_FAST)


    def next_item(self):
        print("next")
        if self.current_selected_item == self.items_per_page:
            print("Last item on page. TODO: Handle")
        self.current_selected_item += 1
        display.set_update_speed(badger2040.UPDATE_TURBO)
        self.list_batches()
        display.set_update_speed(badger2040.UPDATE_FAST)


listing = BeerListing()

def button(pin):
    global changed
    changed = True

    # if pin == badger2040.BUTTON_A:
        #launch_example(0)
    # if pin == badger2040.BUTTON_B:
        #launch_example(1)
    # if pin == badger2040.BUTTON_C:
        #launch_example(2)
    if pin == badger2040.BUTTON_UP:
        listing.previous_item()
    if pin == badger2040.BUTTON_DOWN:
        listing.next_item()



while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    if display.pressed(badger2040.BUTTON_A):
        button(badger2040.BUTTON_A)
    if display.pressed(badger2040.BUTTON_B):
        button(badger2040.BUTTON_B)
    if display.pressed(badger2040.BUTTON_C):
        button(badger2040.BUTTON_C)

    if display.pressed(badger2040.BUTTON_UP):
        button(badger2040.BUTTON_UP)
    if display.pressed(badger2040.BUTTON_DOWN):
        button(badger2040.BUTTON_DOWN)

    display.halt()
