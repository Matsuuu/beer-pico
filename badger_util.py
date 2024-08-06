import badger2040
import network
import time

def clear_screen(display):
    # Clear to white
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

def test_network():
    if not network.WLAN(network.STA_IF).isconnected() :
        display = badger2040.Badger2040()
        display.connect()

def wait_for_user_to_release_buttons(display):
    while display.pressed_any():
        time.sleep(0.01)
