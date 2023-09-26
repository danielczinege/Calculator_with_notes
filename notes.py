from typing import Dict

from PyQt5.QtWidgets import (QMainWindow,
                             QStatusBar, 
                             QTabWidget, 
                             QAction, 
                             QWidget,
                             QPushButton,
                             QTextEdit,
                             QVBoxLayout,
                             QFileDialog,
                             QMessageBox)

from notes_gui import Ui_MainWindow as Notes_window

BYTES_TO_READ = 8 * 1024

class NotesWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Notes_window()
        self.ui.setupUi(self)

        self.text_edits_on_tabs: Dict[str, QTextEdit] = {}

        self.ui.tabWidget.setTabPosition(QTabWidget.South)
        self.tab_count = 0

        self.create_menu_bar()

    def closeEvent(self, event):
        if self.close_all_without_saving_dial():
            event.accept()
        else:
            event.ignore()

    def create_menu_bar(self):
        self.setStatusBar(QStatusBar(self))
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")

        new_action = QAction("New tab", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.add_new)
        file_menu.addAction(new_action)

        open_action = QAction("Open notes", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_notes)
        file_menu.addAction(open_action)

        save_action = QAction('Save notes', self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_notes)
        file_menu.addAction(save_action)

        self.add_new()

    def add_new(self):
        new_tab = QWidget()
        button = QPushButton("Close tab", new_tab)
        button.clicked.connect(self.close_tab)
        text_edit = QTextEdit(new_tab)

        # Create a layout for the new tab's contents
        tab_layout = QVBoxLayout()
        tab_layout.addWidget(button)
        tab_layout.addWidget(text_edit)

        new_tab.setLayout(tab_layout)

        self.tab_count += 1
        name = "Notes " + str(self.tab_count)
        self.ui.tabWidget.addTab(new_tab, name)

        self.text_edits_on_tabs[name] = text_edit

    def open_notes(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)", options=options)

        if file_name and file_name.endswith(".txt"):
            with open(file_name, 'r') as file:
                text = file.read(BYTES_TO_READ)
                self.add_new()
                name = "Notes " + str(self.tab_count)
                self.text_edits_on_tabs[name].setPlainText(text)

    def save_notes(self):
        if self.ui.tabWidget.count() == 0:
            return

        options = QFileDialog.Options()
        options |= QFileDialog.AcceptSave

        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'w') as file:
                index = self.ui.tabWidget.currentIndex()
                text_edit: QTextEdit = self.text_edits_on_tabs[self.ui.tabWidget.tabText(index)]
                text = text_edit.toPlainText()
                file.write(text)

    def close_without_saving_dial(self):
        response = QMessageBox.question(self, "Don't save?", 'Are you sure you want to close the tab without saving?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if response == QMessageBox.No:
            self.save_notes()

    def close_all_without_saving_dial(self) -> bool:
        response = QMessageBox.question(self, "Don't save?", "If you close this window now all unsaved notes will be lost!\n\
Do you really want to close the window without saving?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        return response == QMessageBox.Yes

    def close_tab(self):
        current_tab = self.ui.tabWidget.currentIndex()

        self.close_without_saving_dial()

        name = self.ui.tabWidget.tabText(current_tab)
        self.text_edits_on_tabs.pop(name)

        self.ui.tabWidget.removeTab(current_tab)
