from apps.actions import Actions
from apps.beer import BeerDisplay
from apps.beer_listing import BeerListing
from badger_util import clear_screen
import badger2040
from badger2040 import WIDTH, HEIGHT

display = badger2040.Badger2040()

class Manager:

    def __init__(self):
        print("Initializing Manager")
        self.beer_listing = BeerListing(self)
        self.beer_display = BeerDisplay(self)
        self.check_for_existing_beer()

    def check_for_existing_beer(self):
        beer_state_file = open("/state/selected_beer", "r")
        beer_id = beer_state_file.readline()

        if beer_id is not "":
            action = Actions.GO_TO_BEER_DISPLAY
        else:
            action = Actions.GO_TO_LISTING

        while True:
            print("Manager loop")
            print("Action: " + str(action))

            self.render_loading()

            if action is Actions.GO_TO_LISTING:
                action = self.beer_listing.render()
            elif action is Actions.GO_TO_BEER_DISPLAY:
                beer_state_file = open("/state/selected_beer", "r")
                beer_id = beer_state_file.readline()
                action = self.beer_display.show_beer(beer_id)

    def render_loading(self):
        clear_screen(display)
        text_size = display.measure_text("Loading...", 2)
        display.text("Loading...", round(WIDTH / 2) - round(text_size / 2), round(HEIGHT / 2))
        display.update()

    def go_to_listing(self):
        self.beer_listing.render()

    def go_to_beer_display(self):
        self.check_for_existing_beer()

Manager()
