import badger2040
import urequests
import network

def clear_screen(display):
    # Clear to white
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

def test_network():
    net = network.WLAN(network.STA_IF).ifconfig()
    if net is None:
        display = badger2040.Badger2040()
        display.connect()
