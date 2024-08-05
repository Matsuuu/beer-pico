from service.brewfather import get_batches
import badger2040


display = badger2040.Badger2040()
# Clear to white
display.set_pen(15)
display.clear()

def list_batches():
    batches = get_batches()
    print(batches)

list_batches()

