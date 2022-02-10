import requests
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from ui_yandex_map import Ui_MainWindow


class MiniMap(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setFixedSize(915, 640)
        self.ll = ["37.6156", "55.7522"]
        self.spn = 0.002
        self.l = "map"

        self.if_there_a_point = False
        self.ll_point = [None, None]
        self.map_api_server = "http://static-maps.yandex.ru/1.x/"
        self.search_api_server = "https://search-maps.yandex.ru/v1/"
        self.search_api_server = "https://search-maps.yandex.ru/v1/"
        self.apikey = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)

        self.pushButton_change_view_up.clicked.connect(self.pg_up_image)
        self.pushButton_change_view_down.clicked.connect(self.pg_down_image)
        self.pushButton_move_camera_up.clicked.connect(self.up_image)
        self.pushButton_move_camera_down.clicked.connect(self.down_image)
        self.pushButton_move_camera_left.clicked.connect(self.left_image)
        self.pushButton_move_camera_right.clicked.connect(self.right_image)



    def get_image(self):
        k1, k2 = self.ll
        if not self.if_there_a_point:
            map_request_params = {
                "ll": f"{k1},{k2}",
                "spn": f"{self.spn},{self.spn}",
                "l": f"{self.l}"
            }
        else:
            map_request_params = {
                "ll": f"{k1},{k2}",
                "spn": f"{self.spn},{self.spn}",
                "l": f"{self.l}",
                "pt": "{0},pm2dgl".format("{0},{1}".format(self.ll_point[0], self.ll_point[1]))
            }
        print(self.map_api_server, map_request_params)
        response = requests.get(self.map_api_server, map_request_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
        return map_file

    def pg_up_image(self):
        self.spn = min(90.0, 2 * self.spn)
        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)

    def pg_down_image(self):
        self.spn = max(0.0001, self.spn / 2)
        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)

    def up_image(self):
        self.ll[1] = str(float(self.ll[1]) + self.spn / 2)
        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)

    def down_image(self):
        self.ll[1] = str(float(self.ll[1]) - self.spn / 2)
        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)

    def left_image(self):
        self.ll[0] = str(float(self.ll[0]) - self.spn / 2)
        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)

    def right_image(self):
        self.ll[0] = str(float(self.ll[0]) + self.spn / 2)
        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)








# первая


# вторая



def pg_down_image(k1, k2):
    global spn
    spn -= 0.001
    image = get_image(k1, k2, spn, l)
    return image


# третья



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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MiniMap()
    ex.show()
    sys.exit(app.exec_())