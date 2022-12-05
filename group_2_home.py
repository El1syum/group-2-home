from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QInputDialog, QLineEdit, QWidget, \
    QTableWidget
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QFont
import sys


# TODO Добавит новый класс в котором:
# TODO 1) Добавить заголовок
# TODO 2) подключится к базе данных
# TODO 3) созлать таблицу используя класс QTableWidget()
# TODO 4) создать функцию table_formation в которой будет формироватся таблица
# TODO 5) добавить таблицу в центре окна
# TODO 6) отоброзить все окна

# TODO В методе table_formation:
# TODO 1) добавить количество колонок в таблицу
# TODO 2) добавить название каждой колонки используя метод: setHorizontalHeaderLabels
# TODO 3) выболнить SQL запрос для получения всех данных из базы данных
# TODO 4) с помощью цикла ваил заполнить все ряды в таблице
# TODO 5) изменить размер колонки, в зависимости от контента( аналог sizeHint )


class Table(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Таблица')
        self.resize(700, 800)
        self.initUI()

    def initUI(self):
        pass


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оценочки")
        self.resize(600, 700)
        self.init_ui()

    def init_ui(self):
        self.create_bd()
        self.add_buttons()
        self.show()

    def add_buttons(self):
        mark_button = QPushButton("добавить оценку", self)
        mark_button.resize(mark_button.sizeHint())
        mark_button.move(10, 10)
        mark_button.clicked.connect(self.mark_button)

        student_button = QPushButton("добавить ученика", self)
        student_button.resize(student_button.sizeHint())
        student_button.move(10, 50)
        student_button.clicked.connect(self.data_button)

        db_button = QPushButton('Вывести БД', self)
        db_button.resize(db_button.sizeHint())
        db_button.move(200, 10)
        db_button.clicked.connect(self.db_view)

    def create_bd(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("students.sqlite")
        if not self.db.open():
            print("Не получилось открыть базу :(")
        self.query = QSqlQuery()
        self.query.exec("""CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            mark TEXT)
            """)

    def get_text(self):
        text, ok = QInputDialog.getText(self, "добавление ученика", "Введите имя ученика:", QLineEdit.Normal, "")
        if text != "" and ok:
            return text

    def data_button(self):
        name = self.get_text()
        self.query.prepare("INSERT INTO students (name) VALUES (?)")
        self.query.addBindValue(name)
        self.query.exec()

    def mark_button(self):
        names = self.get_name()
        name = self.get_choice(names)
        if name:
            mark = self.get_mark()
            add_mark = self.get_grade(name, mark)
            self.update_mark(name, add_mark)

    # TODO Добавить функцию db_view которая будет открывать новое окно с базой данных
    def db_view(self): pass

    def update_mark(self, name, mark):
        self.query.prepare("UPDATE students SET mark = (?) WHERE name = (?)")
        self.query.addBindValue(mark)
        self.query.addBindValue(name)
        self.query.exec()

    def get_grade(self, name, mark):
        self.query.prepare("SELECT mark FROM students WHERE name = (?)")
        self.query.addBindValue(name)
        self.query.exec()
        while self.query.next():
            marks = self.query.value(self.query.record().indexOf("mark"))
            marks += f' {mark}'
        return marks

    def get_name(self):
        self.query.prepare("SELECT name FROM students")
        if not self.query.exec():
            print("Не получилось загрузить БД :(", self.query.lastError())
        names = []
        name_index = self.query.record().indexOf("name")
        while self.query.next():
            name = self.query.value(name_index)
            names.append(name)
        return names

    def get_choice(self, names):
        name, ok = QInputDialog.getItem(self, "ученики", "Выберите ученика:", names, 0, False)
        if ok:
            return name
        else:
            return False

    def get_mark(self):
        mark, ok = QInputDialog.getInt(self, "добавить оценку", "Выберите оценку:", 5, 2, 5, 1)
        if ok:
            return mark


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = Window()
    sys.exit(app.exec_())
