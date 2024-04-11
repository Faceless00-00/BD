import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QComboBox, QPushButton, QHBoxLayout, QWidget, QRadioButton, QLabel, QCheckBox, QMessageBox
import pymysql

class DeductionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Выбор типа вычета")
        self.setFixedSize(300, 300)

        layout = QVBoxLayout()

        self.combobox = QComboBox()
        self.btn_update = QPushButton('Обновить')
        self.btn_update.setFixedSize(65, 25)
        self.layout_combobox = QHBoxLayout()
        self.layout_combobox.addWidget(self.combobox)
        self.layout_combobox.addWidget(self.btn_update)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        layout.addLayout(self.layout_combobox)

        # Кнопки
        self.calculate = QPushButton('Рассчитать')
        self.write = QPushButton('Записать')

        # Текст
        self.label_output = QLabel('Текст')
        layout.addWidget(self.label_output)
        name_radio = self.name_radio_buttton()
        self.radio_btn1 = QRadioButton(f'{name_radio[0]}')
        self.radio_btn2 = QRadioButton(f'{name_radio[1]}')

        # Checkbox
        self.name_check = self.name_check_f()
        self.check_0 = QCheckBox(f'{self.name_check[0]}')
        self.check_1 = QCheckBox(f'{self.name_check[1]}')
        self.check_2 = QCheckBox(f'{self.name_check[2]}')

        self.layout_check = QVBoxLayout()
        self.layout_check.addWidget(self.check_0)
        self.layout_check.addWidget(self.check_1)
        self.layout_check.addWidget(self.check_2)
        layout.addLayout(self.layout_check)

        # Добавление радиокнопок
        self.layout_radio = QHBoxLayout()
        self.layout_radio.addWidget(self.radio_btn1)
        self.layout_radio.addWidget(self.radio_btn2)
        layout.addLayout(self.layout_radio)

        self.layout_btn = QHBoxLayout()
        self.layout_btn.addWidget(self.calculate)
        self.layout_btn.addWidget(self.write)
        layout.addLayout(self.layout_btn)

        self.populate_combobox()
        self.calculate.clicked.connect(self.calculate_f)
        self.write.clicked.connect(self.write_f)
        self.btn_update.clicked.connect(self.update_f)

    # Получаем данные для опдейта
    def get_data_for_update(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                out = []
                sql = "SELECT privilege FROM Agents WHERE full_name = %s"
                cursor.execute(sql, (self.combobox.currentText(),))
                agent_priv = [row[0] for row in cursor.fetchall()]
                out += agent_priv
                sql = "SELECT name FROM Children WHERE agent_id = (SELECT id FROM Agents WHERE full_name = %s)"
                cursor.execute(sql, (self.combobox.currentText(),))
                child =  [row [0] for row in cursor.fetchall()]
                if (child == []):
                    out += [0, 0]
                else:
                    out += [1]
                sql = "SELECT privilege FROM Children WHERE agent_id = (SELECT id FROM Agents WHERE full_name = %s)"
                cursor.execute(sql, (self.combobox.currentText(),))
                child_prev = [row [0] for row in cursor.fetchall()]
                out += child_prev
                print(out)
                return out
        except pymysql.Error as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            connection.close()

    # Клик для обдейта
    def update_f(self):
        temp = self.get_data_for_update()
        if not temp[0]:
            self.check_0.hide()
        else:
            self.check_0.show()
        if not temp[1]:
            self.check_1.hide()
        else:
            self.check_1.show()
        if not temp[2]:
            self.check_2.hide()
        else:
            self.check_2.show()
        self.label_output.clear()
        self.check_0.setChecked(False)
        self.check_1.setChecked(False)
        self.check_2.setChecked(False)

    # Получаем имена чекбоксов
    def name_check_f(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM DeductionTypes")
                data_check = [row[0] for row in cursor.fetchall()]
                return data_check
        except pymysql.Error as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            connection.close()

    # Получаем данные для расчета зарплаты
    def get_data_from_table(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                sql = f"CALL get_out_list(%s)"
                cursor.execute(sql, (self.combobox.currentText(),))
                cur = cursor.fetchall()
                id = [row[0] for row in cur]
                price = [row[1] for row in cur]
                out = id + price
                return out
        except pymysql.Error as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            connection.close()

    # Клик записи в бд
    def write_f(self):
        temp = self.get_data_from_table()[1]
        out = temp
        type_oper = 0
        if (self.radio_btn1.isChecked()):
            type_oper = 1
            if self.check_0.isChecked():
                out += temp * (0.01 * self.get_agent_priv())
            else:
                out += 0
            if self.check_1.isChecked():
                out += temp * (0.01 * self.get_child())
            else:
                out += 0
            if self.check_2.isChecked():
                out += temp * (0.01 * self.get_child_priv())
            else:
                out += 0
            self.label_output.setText(f"{out}")

        elif (self.radio_btn2.isChecked()):
            type_oper = 2
            if self.check_0.isChecked():
                out -= temp * (0.01 * self.get_agent_priv())
            else:
                out -= 0
            if self.check_1.isChecked():
                out -= temp * (0.01 * self.get_child())
            else:
                out -= 0
            if self.check_2.isChecked():
                out -= temp * (0.01 * self.get_child_priv())
            else:
                out -= 0
            print(out)
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                cursor.execute(f"CALL AddEarning(NOW(), {out}, {self.get_data_from_table()[0]}, {type_oper})")
            connection.commit()
            QMessageBox.information(self, "Успех", "Данные успешно записаны.")
        except pymysql.Error as e:
            print("Ошибка при записи в базу данных:", e)
        finally:
            connection.close()

    # Получаем размер для расчета вычета для агента
    def get_agent_priv(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                sql = f"SELECT amount FROM DeductionTypes WHERE name = (%s)"
                cursor.execute(sql, (self.check_0.text(),))
                cur = cursor.fetchall()
                amount = [row[0] for row in cur]
                return int(amount[0])
        except pymysql.Error as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            connection.close()

    # Получаем размер для расчета вычета за рёбнка
    def get_child(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                sql = f"SELECT amount FROM DeductionTypes WHERE name = (%s)"
                cursor.execute(sql, (self.check_1.text(),))
                cur = cursor.fetchall()
                amount = [row[0] for row in cur]
                return int(amount[0])
        except pymysql.Error as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            connection.close()

    # Получаем размер для расчета вычета за рёбнка-инвалида
    def get_child_priv(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                sql = f"SELECT amount FROM DeductionTypes WHERE name = (%s)"
                cursor.execute(sql, (self.check_2.text(),))
                cur = cursor.fetchall()
                amount = [row[0] for row in cur]
                return int(amount[0])
        except pymysql.Error as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            connection.close()

    # Расчитываем зарплату в label
    def calculate_f(self):
        self.label_output.clear()
        if (self.radio_btn1.isChecked()):
            temp = self.get_data_from_table()[1]
            out = temp
            if self.check_0.isChecked():
                out += temp * (0.01 * self.get_agent_priv())
            else:
                out += 0
            if self.check_1.isChecked():
                out += temp * (0.01 * self.get_child())
            else:
                out += 0
            if self.check_2.isChecked():
                out += temp * (0.01 * self.get_child_priv())
            else:
                out += 0
            self.label_output.setText(f"{out}")

        elif (self.radio_btn2.isChecked()):
            temp = self.get_data_from_table()[1]
            out = temp
            if self.check_0.isChecked():
                out -= temp * (0.01 * self.get_agent_priv())
            else:
                out -= 0
            if self.check_1.isChecked():
                out -= temp * (0.01 * self.get_child())
            else:
                out -= 0
            if self.check_2.isChecked():
                out -= temp * (0.01 * self.get_child_priv())
            else:
                out -= 0
            self.label_output.setText(f"{out}")

        self.check_0.setChecked(False)
        self.check_1.setChecked(False)
        self.check_2.setChecked(False)

    # Имена для radiobutton
    def name_radio_buttton(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                cursor.execute("SELECT name FROM OperationTypes")
                OperationTypes = [row[0] for row in cursor.fetchall()]
        except pymysql.Error as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            connection.close()
            return OperationTypes

    # Получаем имена для combobox
    def populate_combobox(self):
        try:
            connection = pymysql.connect(
                host="localhost",
                user="root",
                password="",
                database="AdvertisingCompany"
            )
            with connection.cursor() as cursor:
                cursor.execute("SELECT full_name FROM Agents")
                deduction_types = [row[0] for row in cursor.fetchall()]
                self.combobox.addItems(deduction_types)
        except pymysql.Error as e:
            print("Ошибка при получении данных из базы данных:", e)
        finally:
            connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeductionWindow()
    window.show()
    sys.exit(app.exec())
