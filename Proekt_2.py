import sys
from PyQt5.QtWidgets import *
import sqlite3


def handle_exception(exc_type, exc_value, exc_traceback):
    print(exc_type, exc_value, exc_traceback)


sys.excepthook = handle_exception


class Window_2(QWidget):
    def __init__(self):
        super(Window_2, self).__init__()
        self.setGeometry(300, 200, 800, 800)
        self.setWindowTitle('Редактор')
        self.spisok = ["UNIVERSITIES"]
        self.spisok_2 = []
        self.text_2 = ''
        self.connect_to_bd()
        self.initUI()

    def initUI(self):
        self.table = QTableWidget(self)
        self.table.move(0, 40)
        self.table.resize(1920, 585)
        self.combo_1 = QComboBox(self)
        for i in self.spisok:
            self.combo_1.addItem(str(i))
        self.combo_1.move(10, 10)
        self.combo_1.resize(600, 30)
        self.combo_1.activated[str].connect(self.table_apdate)

        self.btn_7 = QPushButton("Сохранить", self)
        self.btn_7.move(10, 750)
        self.btn_7.resize(150, 40)
        self.btn_7.clicked.connect(self.get_data)

    def get_data(self):
        self.spisok_2 = []
        if self.text_2 == "UNIVERSITIES":
            for i in range(self.table.rowCount()):
                if self.table.item(i, 0):
                    self.spisok_2.append((self.table.item(i, 1).text(), self.table.item(i, 0).text()))
        else:
            for i in range(self.table.rowCount()):
                if self.table.item(i, 0) and self.table.item(i, 1).text() and self.table.item(i, 2).text() and \
                        self.table.item(i, 3).text() and self.table.item(i, 3).text() and \
                        self.table.item(i, 5).text():
                    self.spisok_2.append((i + 1, self.table.item(i, 1).text(),
                                          self.table.item(i, 2).text(), self.table.item(i, 3).text(),
                                          self.table.item(i, 4).text(), self.table.item(i, 5).text(), i + 1))
        self.appdate()
        self.connect_to_bd()

    def appdate(self):
        if self.text_2 == "UNIVERSITIES":
            sqlite_update_query_1 = """UPDATE UNIVERSITIES set name=? WHERE id_name=?"""
            sqlite_update_query_2 = """DELETE from UNIVERSITIES where id_name =?"""
            for i in self.spisok_2:
                if i[0] != '':
                    self.cursor_1.execute(sqlite_update_query_1, i)
                    self.bd_1.commit()
                else:
                    self.cursor_1.execute(sqlite_update_query_2, i[1])
                    self.bd_1.commit()

    def table_apdate(self, text):
        self.text_2 = text
        if self.text_2 == "UNIVERSITIES":
            self.table.hide()
            self.result = self.cursor_1.execute(f"""SELECT * FROM UNIVERSITIES""").fetchall()
            self.table = QTableWidget(len(self.result) + 1, len(self.result[0]), self)
            self.table.move(0, 40)
            self.table.resize(1920, 585)
            self.table.setHorizontalHeaderLabels(["id", "Название"])
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(self.result)):
                for j in range(len(self.result[i])):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))
            self.table.show()
        else:
            self.table.hide()
            self.result = self.cursor_1.execute(f"""SELECT ID_university, 
                                            Cр_проходной_балл_бюджет_2021,
                                            Ср_проходной_балл_платно_2021, Бюджетных_мест_2021, 
                                            Платных_мест_2021, Экзамены
                                            FROM Bachelor_and_specialty
                                            
                                             """).fetchall()
            self.table = QTableWidget(len(self.result) + 1, len(self.result[0]), self)
            self.table.move(0, 40)
            self.table.resize(1920, 585)
            self.table.setHorizontalHeaderLabels(
                ["ID_university", "Cр_проходной_балл_бюджет_2021",
                 "Ср_проходной_балл_платно_2021", "Бюджетных_мест_2021",
                 "Платных_мест_2021", "Экзамены"
                 ])
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(self.result)):
                for j in range(len(self.result[0])):
                    self.table.setItem(i, j, QTableWidgetItem(str(self.result[i][j])))
            self.table.show()

    def connect_to_bd(self):
        # Бд названиями Вузов
        self.bd_1 = sqlite3.connect("UNIVERSITIES.db")
        self.cursor_1 = self.bd_1.cursor()
        self.result_1 = self.cursor_1.execute("""SELECT * FROM UNIVERSITIES""").fetchall()
        self.result_2 = self.cursor_1.execute("""SELECT * FROM Bachelor_and_specialty""").fetchall()
