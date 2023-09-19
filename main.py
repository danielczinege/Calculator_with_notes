from PyQt5.QtWidgets import QApplication, QMainWindow, QToolButton, QMenu
from PyQt5.QtCore import QFile, Qt
from calculator_gui import Ui_MainWindow

import pyperclip

from my_eval import evaluation

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.zero_button.clicked.connect(self.writing_buttons)
        self.ui.one_button.clicked.connect(self.writing_buttons)
        self.ui.two_button.clicked.connect(self.writing_buttons)
        self.ui.three_button.clicked.connect(self.writing_buttons)
        self.ui.four_button.clicked.connect(self.writing_buttons)
        self.ui.five_button.clicked.connect(self.writing_buttons)
        self.ui.six_button.clicked.connect(self.writing_buttons)
        self.ui.seven_button.clicked.connect(self.writing_buttons)
        self.ui.eight_button.clicked.connect(self.writing_buttons)
        self.ui.nine_button.clicked.connect(self.writing_buttons)

        self.ui.plus_button.clicked.connect(self.writing_buttons)
        self.ui.minus_button.clicked.connect(self.writing_buttons)
        self.ui.multiply_button.clicked.connect(self.writing_buttons)
        self.ui.divide_button.clicked.connect(self.writing_buttons)

        self.ui.pi_button.clicked.connect(self.writing_buttons)
        self.ui.euler_button.clicked.connect(self.writing_buttons)

        self.ui.mod_button.clicked.connect(self.writing_buttons)
        self.ui.square_button.clicked.connect(self.writing_buttons)
        self.ui.abs_button.clicked.connect(self.writing_buttons)

        self.ui.par_left_button.clicked.connect(self.writing_buttons)
        self.ui.par_right_button.clicked.connect(self.writing_buttons)

        self.ui.del_button.clicked.connect(self.delete_char)
        self.ui.erase_button.clicked.connect(self.erase_input_line)


        self.ui.trig_button.setPopupMode(QToolButton.MenuButtonPopup)
        trig_menu = QMenu(self)

        sin_action = trig_menu.addAction('sin')
        cos_action = trig_menu.addAction('cos')
        tan_action = trig_menu.addAction('tan')
        arcsin_action = trig_menu.addAction('arcsin')
        arccos_action = trig_menu.addAction('arccos')
        arctan_action = trig_menu.addAction('arctan')

        sin_action.triggered.connect(self.writing_buttons)
        cos_action.triggered.connect(self.writing_buttons)
        tan_action.triggered.connect(self.writing_buttons)
        arcsin_action.triggered.connect(self.writing_buttons)
        arccos_action.triggered.connect(self.writing_buttons)
        arctan_action.triggered.connect(self.writing_buttons)

        self.ui.trig_button.setMenu(trig_menu)


        self.ui.invert_button.clicked.connect(self.invert_action)

        self.ui.decimal_point_button.clicked.connect(self.decimal_point)
        self.ui.copy_button.clicked.connect(self.copy_last_result)

        self.ui.more_button.setCheckable(True)
        self.ui.more_button.clicked.connect(self.more_buttons)

        self.ui.root_button.clicked.connect(self.writing_buttons)
        self.ui.log_button.clicked.connect(self.writing_buttons)

        self.ui.equal_button.clicked.connect(self.evaluate)
        self.ui.input_line.returnPressed.connect(self.evaluate)

        self.ui.last_result_label.setTextInteractionFlags(self.ui.last_result_label.textInteractionFlags() | Qt.TextSelectableByMouse)
        self.ui.last_result_label.setCursor(Qt.IBeamCursor)

    def writing_buttons(self):
        """
        This method determins which button made the signal and then writes the coresponding character to input_line.
        """
        sender_button = self.sender().text()
        to_add = ''

        if sender_button == 'π':
            to_add = 'pi '
        elif sender_button == '÷':
            to_add = '/ '
        elif sender_button == 'x':
            to_add = '* '
        elif sender_button == 'x²':
            to_add = '^ 2 '
        elif sender_button == 'xʸ':
            to_add = '^ '
        elif sender_button == '√x':
            to_add = 'sroot '
        elif sender_button.isdigit():
            to_add = sender_button
        else:
            to_add = sender_button + ' '

        new_text = self.ui.input_line.text()
        if len(new_text) == 0 or new_text[-1] == ' ' or ((new_text[-1].isdigit() or new_text[-1] == ',') and to_add.isdigit()):
            new_text += to_add
        else:
            new_text += ' ' + to_add

        self.ui.input_line.setText(new_text)

    def delete_char(self):
        """
        Deletes spaces until it reaches non space character and deletes it.
        """
        old_text = self.ui.input_line.text()
        i = len(old_text) - 1

        while i >= 0 and old_text[i] == ' ':
            i -= 1

        self.ui.input_line.setText(old_text[:i])

    def erase_input_line(self):
        """
        Deletes all characters from input line.
        """
        self.ui.input_line.setText('')

    def invert_action(self):
        """
        Inverts the last number or the last expression in brackets.
        """
        current_text = self.ui.input_line.text()
        i = len(current_text) - 1

        while i >= 0 and current_text[i] == ' ':
            i -= 1

        if i < 0:
            return

        if current_text[i] == 'e' and (i - 1 < 0 or current_text[i - 1] == ' '):
            self.ui.input_line.setText(current_text[:i] + '( 1 / e )')
            return

        if current_text[i] == 'i' and i - 1 >= 0 and current_text[i - 1] == 'p' and (i - 2 < 0 or current_text[i - 2] == ' '):
            self.ui.input_line.setText(current_text[:i - 1] + '( 1 / pi )')
            return

        if not current_text[i].isdigit() and current_text[i] != ')':
            return

        end = i
        decimal_point_found = False

        while i >= 0 and (current_text[i].isdigit() or current_text[i] == ','):
            if decimal_point_found and current_text[i] == ',':
                return

            decimal_point_found = decimal_point_found or current_text[i] == ','
            i -= 1

        if end != i:
            self.ui.input_line.setText(current_text[:i + 1] + '( 1 / ' + current_text[i + 1 : end + 1] + ' ) ')
            return

        i -= 1
        opened_brackets = 1
        while i >= 0 and opened_brackets > 0:
            if current_text[i] == ')':
                opened_brackets += 1
            elif current_text[i] == '(':
                opened_brackets -= 1

            i -= 1

        if opened_brackets > 0:
            return

        self.ui.input_line.setText(current_text[:i + 2] + ' 1 / ( ' + current_text[i + 2 : end].strip() + ' ) )')

    def decimal_point(self):
        """
        Writes a decimal point if and only if the last thing written is a number that does not have a decimal point yet.
        """
        old_text = self.ui.input_line.text()
        if len(old_text) == 0 or not old_text[-1].isdigit():
            return

        i = len(old_text) - 1

        while i >= 0 and old_text[i].isdigit():
            i -= 1

        if i >= 0 and old_text[i] == ',':
            return

        self.ui.input_line.setText(old_text + ',')

    def copy_last_result(self):
        """
        Copies the last result to clipboard.
        """
        pyperclip.copy(self.ui.last_result_label.text())

    def more_buttons(self, checked):
        """
        Switches square root to general root, squaring to general exponentiation and ln to general log.
        """
        if checked:
            self.ui.root_button.setText("yth_root")
            self.ui.square_button.setText("xʸ")
            self.ui.log_button.setText("log_base")
        else:
            self.ui.root_button.setText("√x")
            self.ui.square_button.setText("x²")
            self.ui.log_button.setText("ln")

    def evaluate(self):
        expression = self.ui.input_line.text()
        if expression == "":
            return

        result = evaluation(expression)
        self.ui.last_result_label.setText(result)
        self.ui.input_line.setText(result)

        #TODO - history

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
