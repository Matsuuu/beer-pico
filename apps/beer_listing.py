from apps.actions import Actions
from service.brewfather import get_batches
import badger2040
from badger2040 import HEIGHT, WIDTH
import time

from badger_util import clear_screen, wait_for_user_to_release_buttons


display = badger2040.Badger2040()
display.set_update_speed(badger2040.UPDATE_FAST)

# Approximate center lines for buttons A, B and C
centers = (41, 147, 253)

class BeerListing():

    batches = []
    current_page = 0
    current_selected_item = 0;
    items_per_page = 7

    def __init__(self, manager):
        self.manager = manager

    def render(self):
        clear_screen(display)
        self.batches = get_batches(self.items_per_page)
        self.list_batches()
        return self.main_loop()

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


    def main_loop(self):
        action = None
        while action is None:
            # Sometimes a button press or hold will keep the system
            # powered *through* HALT, so latch the power back on.
            display.keepalive()

            if display.pressed(badger2040.BUTTON_C):
                action = "select_item"
                wait_for_user_to_release_buttons(display)
                break
            if display.pressed(badger2040.BUTTON_UP):
                self.previous_item()
            if display.pressed(badger2040.BUTTON_DOWN):
                self.next_item()

            display.halt()

        print("Loop escaped")

        if action is "select_item":
            return self.select_item()


    def previous_item(self):
        if self.current_selected_item == 0 and self.current_page == 0:
            return
        if self.current_selected_item == 0 and self.current_page > 0:
            self.current_page -= 1

        self.current_selected_item -= 1
        display.set_update_speed(badger2040.UPDATE_TURBO)
        self.list_batches()
        display.set_update_speed(badger2040.UPDATE_FAST)


    def next_item(self):
        if self.current_selected_item == self.items_per_page:
            print("Last item on page. TODO: Handle")
        self.current_selected_item += 1
        display.set_update_speed(badger2040.UPDATE_TURBO)
        self.list_batches()
        display.set_update_speed(badger2040.UPDATE_FAST)

    def select_item(self):
        state_file = open("/state/selected_beer", "w")
        state_file.write(self.batches[(self.current_page + 1) * self.current_selected_item]["_id"])
        state_file.close()
        return Actions.GO_TO_BEER_DISPLAY

