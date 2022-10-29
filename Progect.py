import sqlite3 as sq
import requests
from bs4 import BeautifulSoup as Bs


class CreateBd:
    def __init__(self, new):
        self.page = 1
        self.l_1, self.l_2, self.l_3, self.l_4 = [], [], [], []
        self.count = 1
        self.dp_1, self.dp_2, self.dp_3, self.dp_4 = None, None, None, None
        self.exams = []
        self.spisok = []
        self.number = 0
        self.result = []
        self.chek_1, self.chek_2 = 0, 0
        self.new = new

    def chek(self):
        conn = sq.connect('UNIVERSITIES.db')
        c = conn.cursor()
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='UNIVERSITIES'
        ''')
        if c.fetchone()[0] == 0:
            self.chek_1 = 0
        else:
            self.chek_1 = 1
        c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Bachelor_and_specialty'
                ''')
        if c.fetchone()[0] == 0:
            self.chek_2 = 0
        else:
            self.chek_2 = 1
        conn.close()
        self.create_info()

    def create_info(self):
        for i in range(1, 5):
            r = requests.get("https://spb.postupi.online/vuzi/?page_num=" + str(i))
            html = Bs(r.content, 'html.parser')
            items = html.find_all('li', class_="list")
            for item in items:
                links = item.find("div", class_="dropdown-menu btn-ddown__menu").find_all()
                c = item.find("div", class_="dropdown-menu btn-ddown__menu").get_text().split(', ')
                if 'Бакалавриат' in c:
                    url = str(links[0])[9:-30]
                else:
                    url = None
                if ('специалитетМагистратура' or 'Магистратура') in c:
                    url_2 = str(links[1])[9:-18]
                else:
                    url_2 = None
                self.l_1.append(item.find('h2', class_="list__h").get_text())
                self.l_2.append(url)
                self.l_3.append(url_2)
                self.l_4.append(self.count)
                self.count += 1
        self.create_bd_1()
        self.create_bd_2()

    def create_bd_1(self):
        if self.chek_1 == 0 or self.new:
            with sq.connect("UNIVERSITIES.db") as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS UNIVERSITIES (
                    id_name INTEGER PRIMARY KEY,
                    name TEXT
                    )""")
            con.commit()
            for i in range(len(self.l_4)):
                con.execute("INSERT INTO UNIVERSITIES VALUES(?, ?)", (self.l_4[i], self.l_1[i]))
            con.commit()

    def create_bd_2(self):
        if self.chek_2 == 0 or self.new:
            with sq.connect("UNIVERSITIES.db") as con:
                cur = con.cursor()
                cur.execute("""CREATE TABLE IF NOT EXISTS Bachelor_and_specialty (
                    ID_university INTEGER,
                    Название_факультета TEXT,
                    Cр_проходной_балл_бюджет_2021 INTEGER,
                    Ср_проходной_балл_платно_2021 INTEGER,
                    Бюджетных_мест_2021 INTEGER,
                    Платных_мест_2021 INTEGER,
                    Экзамены TEXT,
                    FOREIGN KEY (ID_university) REFERENCES UNIVERSITIES (id_name)
                    )""")
            con.commit()

            for i in range(len(self.l_1)):
                link = self.l_2[i]
                page = 1
                if link:
                    while True:
                        count = 1
                        r = requests.get(f'{link} + "?page_num=" + {str(page)}')
                        html = Bs(r.content, 'html.parser')
                        items = html.find_all('div', class_="flex-nd list__info-inner")
                        if len(items):
                            for item in items:
                                url = requests.get(item.find("h2", class_="list__h").find("a").get("href"))
                                html_2 = Bs(url.content, 'html.parser')
                                items_2 = html_2.find("h1", class_="bg-nd__h").get_text().split(",")
                                name = ''
                                for i_2 in range(len(items_2) - 1):
                                    name += items_2[i_2]
                                items_time = html_2.find("section", class_="section-box overflow-wrap")
                                tests = items_time.find("div",
                                                        class_="score-box swiper-slide 0").find_all("p",
                                                                                                    class_=None)
                                self.exams = ""
                                for p in tests:
                                    f = p.get_text()
                                    if "или" in f:
                                        self.exams += f[4:] + ';'
                                    else:
                                        self.exams += f[:-1] + ';'
                                chisla = item.find("div", class_="list__score-wrap").find_all("b")
                                if len(chisla) == 8:
                                    self.dp_1 = str(chisla[4])[3:-4]
                                    self.dp_2 = str(chisla[5])[3:-4]
                                    self.dp_3 = str(chisla[6])[3:-4]
                                    self.dp_4 = str(chisla[7])[3:-4]
                                elif len(chisla) == 6:
                                    self.dp_1 = None
                                    self.dp_2 = str(chisla[3])[3:-4]
                                    self.dp_3 = None
                                    self.dp_4 = str(chisla[5])[3:-4]
                                self.spisok = [i + 1, name, self.dp_1,
                                               self.dp_2, self.dp_3, self.dp_4,
                                               self.exams
                                               ]
                                if self.spisok not in self.result:
                                    self.result.append(self.spisok)
                                    con.execute("INSERT INTO Bachelor_and_specialty VALUES(?, ?, ?, ?, ?, ?, ?)",
                                                self.spisok)
                                con.commit()
                                count += 1
                            page += 1
                            self.number = i + 1
                            print(i + 1, page - 1, count)
                        else:
                            break
