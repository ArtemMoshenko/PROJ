import requests
import sys
spn = 0.002
l = "map"
if_there_a_point = False
ll_point = None
map_api_server = "http://static-maps.yandex.ru/1.x/"
search_api_server = "https://search-maps.yandex.ru/v1/"
apikey = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

# первая
def get_image(k1, k2, spn_loc, l_loc):
    if if_there_a_point:
        map_request_params = {
            "ll": f"{k1},{k2}",
            "spn": f"{spn_loc}",
            "l": f"{l_loc}"
        }
    else:
        map_request_params = {
            "ll": f"{k1},{k2}",
            "spn": f"{spn_loc}",
            "l": f"{l_loc}",
            "pt": "{0},pm2dgl".format("{0},{1}".format(ll_point[0], ll_point[1]))
        }

    response = requests.get(map_api_server, map_request_params)
    if not response:
        print("Ошибка выполнения запроса:")
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file

# вторая
def pg_up_image(k1, k2):
    global spn
    spn += 0.001
    image = get_image(k1, k2, spn, l)
    return image


def pg_down_image(k1, k2):
    global spn
    spn -= 0.001
    image = get_image(k1, k2, spn, l)
    return image


# третья
def up_image(k1, k2):
    image = get_image(k1, k2+spn, spn, l)
    return image


def down_image(k1, k2):
    image = get_image(k1, k2 - spn, spn, l)
    return image


def left_image(k1, k2):
    image = get_image(k1+spn, k2, spn, l)
    return image


def right_image(k1, k2):
    image = get_image(k1-spn, k2, spn, l)
    return image

# 4-ая
def change_l_image(k1, k2, s):
    if s != "map" and s != "sat" and s != "skl":
        return None
    image = get_image(k1, k2, spn, l)
    return image

# 5-ая не до конца
def add_point(k1, k2):
    global if_there_a_point, ll_point
    if_there_a_point = True
    ll_point = [k1, k2]
