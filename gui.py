import sys

from PySide6.QtWidgets import (QWidget, QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
                               QHBoxLayout, QLineEdit, QTextEdit)
from PySide6.QtGui import QIcon, QPixmap

from parcer import scrape_data


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Parcer hotel")
        self.setWindowIcon(QIcon("icon.png"))
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # label = QLabel(self)
        # pixmap = QPixmap("icon.png")
        # label.setPixmap(pixmap)
        # label.adjustSize()
        main_layout = QVBoxLayout(central_widget)

        input_layout = QHBoxLayout()
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("input city name")
        self.city_input.setFixedHeight(50)
        self.search_button = QPushButton('search')
        self.search_button.clicked.connect(self.start_parcing)
        self.search_button.setFixedHeight(50)
        self.search_button.setStyleSheet("font-size: 20px; background-color: blue")

        input_layout.addWidget(QLabel('City'))
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.search_button)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        # self.result_box.setStyleSheet("""
        #             QWidget {
        #             background-image: url("icon.png");
        #             background-repeat: no-repeat;
        #             background-position: center;
        #             background-size: cover;
        #             background-blend-mode: lighten;
        #             }
        #         """)

        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.result_box)

    def start_parcing(self):
        city = self.city_input.text()
        if not city:
            self.result_box.setText("Please enter a city name")
            return
        self.result_box.setText(f"Searching for {city}\n")

        try:
            hotels = scrape_data(city)
            if hotels:
                for hotel in hotels:
                    result = f'{hotel["title"]} - {hotel["price"]}'
                    self.result_box.append(result)
                else:
                    self.result_box.append('No hotel found')
        except Exception as e:
            self.result_box.append(f"error parcing: {e}")
        # self.result_box.append('The best hotel ever =)')



