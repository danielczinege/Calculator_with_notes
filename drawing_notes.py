import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

MAX_TEXT_LENGTH = 50

class TextInputDialog(QtWidgets.QDialog):
    def __init__(self, max_length):
        super().__init__()

        self.setWindowTitle("Text Input")
        self.setFixedSize(300, 100)

        self.label = QtWidgets.QLabel("Enter text: (at most " + str(max_length) + " characters)")
        self.text_input = QtWidgets.QLineEdit()
        self.text_input.setMaxLength(max_length)  # Set the maximum length
        self.ok_button = QtWidgets.QPushButton("OK")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)

class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(700, 100)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)

        self.init_pixmap()

        self.drawing_mode = True

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')
        self.current_width = 2

        self.set_drawing_cursor()

    def set_drawing_cursor(self):
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def set_writing_cursor(self):
        self.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))

    def init_pixmap(self):
        self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap.fill(Qt.white)
        self.setPixmap(self.pixmap)

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def draw_rounded_line(self, painter, x1, y1, x2, y2):
        p = painter.pen()
        p.setWidth(self.current_width)
        p.setColor(self.pen_color)
        painter.setPen(p)

        painter.drawLine(x1, y1, x2, y2)

        # Draw circles at the endpoints for rounded ends
        radius = self.current_width // 8
        painter.setBrush(self.pen_color)
        painter.drawEllipse(QtCore.QPoint(x1 - radius,y1), radius, radius)
        painter.drawEllipse(QtCore.QPoint(x2 + radius,y2), radius, radius)

    def mouseMoveEvent(self, e):
        if not self.drawing_mode:
            return

        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return

        painter = QtGui.QPainter(self.pixmap)

        self.draw_rounded_line(painter, self.last_x, self.last_y, e.x(), e.y())

        self.setPixmap(self.pixmap)
        self.update()

        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def draw_text(self, painter, text, x, y):
        p = painter.pen()
        p.setColor(self.pen_color)
        painter.setPen(p)
        font = painter.font()
        font.setPointSize(20)
        painter.setFont(font)
        painter.drawText(x, y, text)

    def mouseDoubleClickEvent(self, e):
        if self.drawing_mode:
            return

        text_input_dialog = TextInputDialog(MAX_TEXT_LENGTH)
        result = text_input_dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            text = text_input_dialog.text_input.text()
            painter = QtGui.QPainter(self.pixmap)
            self.draw_text(painter, text, e.x(), e.y())
            self.setPixmap(self.pixmap)
            self.update()

COLORS = [
# 17 undertones https://lospec.com/palette-list/17undertones
'#000000', '#141923', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
'#458352', '#dcd37b', '#fffee5', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
'#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]

BLACK = "#141923"

SIZES = [1,2,4,8,16,32]

class QPaletteButton(QtWidgets.QPushButton):
    def __init__(self, color):
        super().__init__()
        self.setFixedSize(QtCore.QSize(24,24))
        self.color = color
        self.setStyleSheet("background-color: %s;" % color)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.canvas = Canvas()

        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)

        palette = QtWidgets.QHBoxLayout()

        self.switch_text_drawing = QtWidgets.QToolButton()
        self.switch_text_drawing.setFixedSize(QtCore.QSize(24,24))
        self.switch_text_drawing.setCheckable(True)
        self.switch_text_drawing.setText("A")

        self.switch_text_drawing.clicked.connect(self.change_mode)

        palette.addWidget(self.switch_text_drawing)

        self.add_palette_buttons(palette)

        self.add_size_buttons(palette)

        l.addLayout(palette)

        l.addWidget(self.canvas)

        self.setCentralWidget(w)
        self.setWindowTitle("Drawing notes")

        self.create_menu_bar()

    def closeEvent(self, event):
        if self.close_without_saving_dial():
            event.accept()
        else:
            event.ignore()

    def close_without_saving_dial(self) -> bool:
        response = QtWidgets.QMessageBox.question(self, "Don't save?", "If you close this window now all unsaved notes will be lost!\n\
Do you really want to close the window without saving?",
                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        return response == QtWidgets.QMessageBox.Yes

    def clear_notes_without_saving(self, text):
        response = QtWidgets.QMessageBox.question(self, "Don't save?", text,
                                                  QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        return response == QtWidgets.QMessageBox.Yes

    def create_menu_bar(self):
        self.setStatusBar(QtWidgets.QStatusBar(self))
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        open_action = QtWidgets.QAction("Open notes", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.load_image)
        file_menu.addAction(open_action)

        save_action = QtWidgets.QAction('Save notes', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)

        delete_action = QtWidgets.QAction('Clear notes', self)
        delete_action.triggered.connect(self.delete_notes)
        file_menu.addAction(delete_action)

    def save_image(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg);;PNG Images (*.png);;JPEG Images (*.jpg)",
                                                             options=options)
        if file_name:
            self.canvas.pixmap.save(file_name)

    def load_image(self):
        if self.clear_notes_without_saving("Would you like to save the notes first before openning new ones?"):
            self.save_image()

        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load Image", "", "Images (*.png *.jpg);;PNG Images (*.png);;JPEG Images (*.jpg)",
                                                             options=options)
        if file_name:
            image = QtGui.QImage(file_name)
            if not image.isNull():
                self.canvas.pixmap = QtGui.QPixmap.fromImage(image)
                self.canvas.setPixmap(self.canvas.pixmap)
                self.canvas.update()
                self.resizeEvent(None)

    def delete_notes(self):
        if self.clear_notes_without_saving("Would you like to save current notes first before clearing them?"):
            self.save_image()

        self.canvas.init_pixmap()

    def change_mode(self, checked):
        if checked:
            self.canvas.drawing_mode = False
            self.canvas.set_writing_cursor()
        else:
            self.canvas.drawing_mode = True
            self.canvas.set_drawing_cursor()

    def add_palette_buttons(self, layout):
        for c in COLORS:
            b = QPaletteButton(c)
            b.pressed.connect(lambda c=c: self.canvas.set_pen_color(c))
            layout.addWidget(b)

    def set_size(self, size):
        self.canvas.current_width = size

    def add_size_buttons(self, layout):
        for size in SIZES:
            b = QtWidgets.QPushButton()
            b.setFixedSize(QtCore.QSize(size + 1, size + 1))
            b.setStyleSheet("background-color: %s; padding: 10px; border: 8px solid %s;" % (BLACK, BLACK))
            b.pressed.connect(lambda size = size: self.set_size(size))
            layout.addWidget(b)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        current_pixmap = self.canvas.pixmap

        new_size = self.canvas.size()
        new_pixmap = QtGui.QPixmap(new_size)
        new_pixmap.fill(Qt.white)

        painter = QtGui.QPainter(new_pixmap)
        painter.drawPixmap(
            QtCore.QRect(0, 0, new_size.width(), new_size.height()),
            current_pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.FastTransformation)
        )

        self.canvas.pixmap = new_pixmap
        self.canvas.setPixmap(new_pixmap)

        painter.end()
