from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt

class Canvas(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(700, 100)

        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Expanding)
        self.setSizePolicy(size_policy)

        self.init_pixmap()

        self.last_x, self.last_y = None, None
        self.pen_color = QtGui.QColor('#000000')
        self.current_width = 2

    def init_pixmap(self):
        self.pixmap = QtGui.QPixmap(self.size())
        self.pixmap.fill(Qt.white)
        self.setPixmap(self.pixmap)

    def set_pen_color(self, c):
        self.pen_color = QtGui.QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None:
            self.last_x = e.x()
            self.last_y = e.y()
            return

        painter = QtGui.QPainter(self.pixmap)
        p = painter.pen()
        p.setWidth(self.current_width)
        p.setColor(self.pen_color)
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.setPixmap(self.pixmap)
        self.update()

        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

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
        self.add_palette_buttons(palette)

        self.add_size_buttons(palette)

        l.addLayout(palette)

        l.addWidget(self.canvas)

        self.setCentralWidget(w)

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
            b.setFixedSize(QtCore.QSize(size, size))
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
