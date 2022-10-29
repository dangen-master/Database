import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
import sqlite3
from Progect import CreateBd
from Proekt_2 import Window_2
import os


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle('Поиск Вуза')
        self.sort_spisok_1 = []
        self.sort_spisok_2 = []
        self.connect_to_bd()
        self.spisok_1, self.spisok_2 = [], []
        self.spisok_3 = []
        self.initUI()  # основное окно программы

    def update_btn(self):
        self.result_1 = self.cursor_1.execute("""SELECT * FROM UNIVERSITIES""").fetchall()
        self.result_2 = self.cursor_1.execute("""SELECT * FROM Bachelor_and_specialty""").fetchall()
        self.spisok_1 = []
        for i in self.result_1:
            self.spisok_1.append(i[1])
        sorted(self.spisok_1)
        print(self.spisok_1)

        self.spisok_2 = []
        self.spisok_3 = []
        for i in self.result_2:
            self.spisok_3.append((i[1], i[6]))
            a = i[6].split(";")
            self.spisok_2 += a
        self.spisok_2 = set(self.spisok_2)
        self.spisok_2.remove('')
        sorted(self.spisok_2)
        self.combo_1.clear()
        for i in self.spisok_1:
            self.combo_1.addItem(str(i))
        self.combo_2.clear()
        print(self.spisok_2)
        for i in self.spisok_2:
            self.combo_2.addItem(str(i))

    def initUI(self):
        # Кнопка выхода
        self.btn_1 = QPushButton('Quit', self)
        self.btn_1.resize(100, 50)
        self.btn_1.move(1820, 1030)
        self.btn_1.clicked.connect(QCoreApplication.instance().quit)

        # пероначальный вывод  в таблицу
        self.result = self.cursor_1.execute("""SELECT * FROM UNIVERSITIES""").fetchall()
        self.table = QTableWidget(len(self.result), len(self.result[0]) - 1, self)
        self.table.resize(1920, 585)
        self.table.setHorizontalHeaderLabels(["Название"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(self.result)):
            for j in range(len(self.result[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][1])))

        # 1 бокс для выборки по
        # конкретным вузам
        self.combo_1 = QComboBox(self)
        for i in self.spisok_1:
            self.combo_1.addItem(str(i))
        self.combo_1.move(10, 650)
        self.combo_1.resize(600, 30)
        self.combo_1.activated[str].connect(self.to_text_1)

        # 1 Окно для ввода вузов по которым происходит фильтрация
        self.input_1 = QLineEdit(self)
        self.input_1.move(10, 610)
        self.input_1.resize(570, 30)
        self.input_1.setEnabled(False)

        # Кнопка очищения окошка 1
        self.btn_2 = QPushButton('X', self)
        self.btn_2.move(580, 610)
        self.btn_2.resize(30, 30)
        self.btn_2.clicked.connect(self.dell_input_1)

        # 2 бокс для выборки по экзаменам
        self.combo_2 = QComboBox(self)
        for i in self.spisok_2:
            self.combo_2.addItem(str(i))
        self.combo_2.move(620, 650)
        self.combo_2.resize(600, 30)
        self.combo_2.activated[str].connect(self.to_text_2)

        # 2 Окно для ввода вузов по которым происходит фильтрация
        self.input_2 = QLineEdit(self)
        self.input_2.move(620, 610)
        self.input_2.resize(570, 30)
        self.input_2.setEnabled(False)

        # Кнопка очищения окошка 2
        self.btn_3 = QPushButton('X', self)
        self.btn_3.move(1190, 610)
        self.btn_3.resize(30, 30)
        self.btn_3.clicked.connect(self.dell_input_2)

        # бюджетные мест
        self.ed1 = QCheckBox(self)
        self.ed1.move(1250, 610)
        self.ed1.setText('Есть бюджетные места')
        self.ed1.adjustSize()

        # кнопка применения фильтров
        self.btn_4 = QPushButton(self)
        self.btn_4.move(10, 700)
        self.btn_4.setText("Применить")
        self.btn_4.adjustSize()
        self.btn_4.clicked.connect(self.apply_table)

        # Кнопка сброса таблицы
        self.btn_5 = QPushButton(self)
        self.btn_5.move(120, 700)
        self.btn_5.setText("Сброс")
        self.btn_5.adjustSize()
        self.btn_5.clicked.connect(self.clear_table)

        self.btn_6 = QPushButton("Редактировать таблицы", self)
        self.btn_6.move(180, 750)
        self.btn_6.resize(150, 40)
        self.btn_6.clicked.connect(self.redact_teble)

        self.btn_7 = QPushButton("Пересоздать таблицы", self)
        self.btn_7.move(10, 750)
        self.btn_7.resize(150, 40)
        self.btn_7.clicked.connect(self.appdate)

    def redact_teble(self):
        self.form = Window_2()
        self.form.show()  # открытие формыsw

    def appdate(self):
        self.bd_1.close()
        self.btn_1.setEnabled(False)
        self.btn_2.setEnabled(False)
        self.btn_3.setEnabled(False)
        self.btn_4.setEnabled(False)
        self.btn_5.setEnabled(False)
        self.btn_6.setEnabled(False)
        self.btn_7.setEnabled(False)
        self.combo_1.setEnabled(False)
        self.combo_2.setEnabled(False)
        self.ed1.setEnabled(False)
        if os.path.isfile("UNIVERSITIES.db"):
            os.remove("UNIVERSITIES.db")
        CreateBd(True).chek()
        self.btn_1.setEnabled(True)
        self.btn_2.setEnabled(True)
        self.btn_3.setEnabled(True)
        self.btn_4.setEnabled(True)
        self.btn_5.setEnabled(True)
        self.btn_7.setEnabled(True)
        self.btn_7.setEnabled(True)
        self.combo_1.setEnabled(True)
        self.combo_2.setEnabled(True)
        self.ed1.setEnabled(True)
        self.connect_to_bd()

    def apply_table(self):
        self.update_btn()
        self.table.hide()
        if not self.sort_spisok_1:
            self.sort_spisok_1 = self.spisok_1
        if not self.sort_spisok_2:
            self.sort_spisok_2 = ' '
        if not self.ed1.isChecked():
            chek = ''
        else:
            chek = 'and "Бюджетных_мест_2021" is not NULL'

        self.table.hide()
        self.result = []
        for i in self.sort_spisok_1:
            for i_2 in self.sort_spisok_2:
                a = self.cursor_1.execute(f"""SELECT UNIVERSITIES.name, Название_факультета, 
                Cр_проходной_балл_бюджет_2021,
                Ср_проходной_балл_платно_2021, Бюджетных_мест_2021, Платных_мест_2021, Экзамены
                FROM Bachelor_and_specialty
                INNER JOIN UNIVERSITIES ON UNIVERSITIES.id_name = Bachelor_and_specialty.ID_university
                WHERE UNIVERSITIES.name = "{i}" {chek} and "Экзамены" Like '%{i_2}%'
                 """).fetchall()
                for i_3 in a:
                    if i_3 not in self.result:
                        self.result.append(i_3)
        if not self.result:
            self.result += self.cursor_1.execute(f"""SELECT UNIVERSITIES.name, Название_факультета, 
                            Cр_проходной_балл_бюджет_2021,
                            Ср_проходной_балл_платно_2021, Бюджетных_мест_2021, Платных_мест_2021, Экзамены
                            FROM Bachelor_and_specialty
                            INNER JOIN UNIVERSITIES ON UNIVERSITIES.id_name = Bachelor_and_specialty.ID_university
                             """).fetchall()
        self.table = QTableWidget(len(self.result), len(self.result[0]), self)
        self.table.resize(1920, 585)
        self.table.setHorizontalHeaderLabels(["Название вуза", "Название_факультета", "Cр_проходной_балл_бюджет_2021",
                                              "Ср_проходной_балл_платно_2021", "Бюджетных_мест_2021",
                                              "Платных_мест_2021", "Экзамены"
                                              ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(self.result)):
            for j in range(len(self.result[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))
        self.table.show()

    def clear_table(self):
        self.table.hide()
        self.result = self.cursor_1.execute("""SELECT * FROM UNIVERSITIES""").fetchall()
        self.table = QTableWidget(len(self.result), len(self.result[0]) - 1, self)
        self.table.resize(1920, 585)
        self.table.setHorizontalHeaderLabels(["Название"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(len(self.result)):
            for j in range(len(self.result[0])):
                self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][1])))
        self.table.show()

    # Заполнения окна ввода 1
    def to_text_1(self, text):
        if text not in self.sort_spisok_1:
            self.sort_spisok_1.append(text)
        self.input_1.setText(";".join(self.sort_spisok_1))

    # Заполнения окна ввода 2
    def to_text_2(self, text):
        if text not in self.sort_spisok_2:
            self.sort_spisok_2.append(text)
        self.input_2.setText(";".join(self.sort_spisok_2))

    # удаление данных из окна ввода 1
    def dell_input_1(self):
        self.sort_spisok_1 = []
        self.input_1.setText('')

    # удаление данных из окна ввода 1
    def dell_input_2(self):
        self.sort_spisok_2 = []
        self.input_2.setText('')

    def connect_to_bd(self):
        # Бд названиями Вузов
        self.bd_1 = sqlite3.connect("UNIVERSITIES.db")
        self.cursor_1 = self.bd_1.cursor()
        try:
            self.result_1 = self.cursor_1.execute("""SELECT * FROM UNIVERSITIES""").fetchall()
            self.result_2 = self.cursor_1.execute("""SELECT * FROM Bachelor_and_specialty""").fetchall()
        except sqlite3.OperationalError:
            if os.path.isfile("UNIVERSITIES.db"):
                os.remove("UNIVERSITIES.db")
            CreateBd(True).chek()


def main_window():
    app = QApplication(sys.argv)  # Подстраиваем окно под операционную систему
    window = Window()
    window.showFullScreen()  # Во весь экран
    window.show()  # Показ окна
    sys.exit(app.exec_())  # коректное завершение программы


if __name__ == "__main__":
    main_window()
