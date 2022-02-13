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
        self.search_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.apikey = "40d1649f-0493-4b70-98ba-98533de7710b"


        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)

        self.pushButton_change_view_up.clicked.connect(self.pg_up_image)
        self.pushButton_change_view_down.clicked.connect(self.pg_down_image)
        self.pushButton_move_camera_up.clicked.connect(self.up_image)
        self.pushButton_move_camera_down.clicked.connect(self.down_image)
        self.pushButton_move_camera_left.clicked.connect(self.left_image)
        self.pushButton_move_camera_right.clicked.connect(self.right_image)
        self.pushButton_start.clicked.connect(self.find_object)
        self.pushButton_clear.clicked.connect(self.clear_object)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)

        self.action_map_view.triggered.connect(self.change_l_image)
        self.action_sat_view.triggered.connect(self.change_l_image)
        self.action_skl_view.triggered.connect(self.change_l_image)



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

    def change_l_image(self):
        s = self.sender().text()
        self.l = s
        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)

    def find_object(self):
        text = self.lineEdit_search.text()
        text.replace(" ", "+")
        request_params = {
            "apikey": self.apikey,
            "geocode": text,
            "format": "json"
        }
        response = requests.get(self.search_api_server, params=request_params)
        if response:
            # Запрос успешно выполнен, печатаем полученные данные.
            json_response = response.json()
            ll_point = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            ll_needed = ll_point["Point"]["pos"]

            print(ll_point["boundedBy"]["Envelope"]["lowerCorner"])
            spn_search_lower = list(map(float, ll_point["boundedBy"]["Envelope"]["lowerCorner"].split()))
            spn_search_upper = list(map(float, ll_point["boundedBy"]["Envelope"]["upperCorner"].split()))
            self.spn = max(abs(spn_search_lower[0] - spn_search_upper[0]), abs(spn_search_lower[1] - spn_search_upper[1]))
            self.ll_point = ll_needed.split(" ")
            self.if_there_a_point = True
            self.ll = ll_needed.split(" ")
            self.pixmap = QPixmap(self.get_image())
            self.label_image.setPixmap(self.pixmap)
            print(ll_needed)
            # print(response.content)
        else:
            # Произошла ошибка выполнения запроса. Обрабатываем http-статус.
            print("Ошибка выполнения запроса:")
            print(request_params)
            print("Http статус:", response.status_code, "(", response.reason, ")")

    def clear_object(self):
        self.if_there_a_point = False
        self.ll_point = [None, None]
        self.pixmap = QPixmap(self.get_image())
        self.label_image.setPixmap(self.pixmap)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MiniMap()
    ex.show()
    sys.exit(app.exec_())