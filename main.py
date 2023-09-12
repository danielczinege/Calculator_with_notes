from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QFile
from calculator_gui import Ui_MainWindow

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


if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
