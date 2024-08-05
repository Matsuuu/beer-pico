import badger2040
import urequests
from BREWFATHER_CONFIG import API_KEY, USER_ID
import ubinascii
import json

BATCHES_URL = "https://api.brewfather.app/v2/batches?order_by=batchNo&order_by_direction=desc&include=recipe.style.name&limit=6"
BATCH_URL = "https://api.brewfather.app/v2/batches/"
BATCH_URL_OPTIONS="?include=measuredAbv,measuredOg,measuredFg,estimatedIbu,recipe.name,recipe.style.name,batchHops"
RECIPES_URL = ""

def get_brewfather_token():
    token = ubinascii.b2a_base64(USER_ID + ":" + API_KEY)
    return token.decode("utf-8")


def get_batches():
    r = urequests.get(BATCHES_URL, headers = { "authorization": "Basic " + get_brewfather_token() })

    res = r.text
    fixed_json_string = "{ \"batches\": " + res + "}"

    batches = json.loads(fixed_json_string)
    return batches

def get_batch_info(batch_id):
    request_url = BATCH_URL + batch_id + BATCH_URL_OPTIONS

    r = urequests.get(request_url, headers = { "authorization": "Basic " + get_brewfather_token() })

    json_data = r.json()

    print(json_data)

    return {
        "id": json_data["_id"],
        "brewer": json_data["brewer"],
        "name": json_data["recipe"]["name"],
        "style": json_data["recipe"]["style"]["name"],
        "abv": json_data.get("measuredAbv"),
        "og": json_data.get("measuredOg"),
        "fg": json_data.get("measuredFg"),
        "ibu": json_data.get("estimatedIbu"),
        "hops": get_hops_from_batch(json_data)
    }

def get_hops_from_batch(batch):
    hops = batch.get("batchHops")
    return [hop.get("name") for hop in hops]
