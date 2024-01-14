from sys import argv, exit
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QWidget
from ui import Ui_H
import xml.etree.ElementTree as ET
from text_formatter import TextFormatter
from data_handler import DataHandler

class TextAnnotationApp(QWidget, Ui_H):
    def __init__(self):
        super(TextAnnotationApp, self).__init__()
        self.setWindowFlags(
            Qt.WindowMinimizeButtonHint |     # enable minimize
            Qt.WindowCloseButtonHint |        # enable close
            Qt.WindowMaximizeButtonHint |     # enable maximize
            Qt.WindowStaysOnTopHint           # enable top always
        )
    
        self.load_config()
        self.format_text = TextFormatter(self.keyword1, self.keyword2).format

        self.dh = DataHandler(self.file_path, self.encoding, self.text_column, self.label_column)
        self.load_data()

        self.setupUi(self)
        self.go_to_unlabeled()
        self.build_link()
    
    def load_config(self):
        tree = ET.parse("config.xml")
        root = tree.getroot()

        self.file_path = root.find("file_path").text
        self.encoding = root.find("encoding").text

        self.keyword1 = root.find("keyword1").text.split(',')
        self.keyword2 = root.find("keyword2").text.split(',')

        self.text_column = root.find("text_column").text
        self.label_column = root.find("label_column").text
    
    def build_link(self):
        self.previous_button.clicked.connect(self.go_to_previous)
        self.next_button.clicked.connect(self.go_to_next)
        self.label_0_button.clicked.connect(lambda: self.label_text(0))
        self.label_1_button.clicked.connect(lambda: self.label_text(1))

        self.setFocusPolicy(Qt.StrongFocus)
    
    def go_to_unlabeled(self):
        self.current_index = 0
        for i in range(len(self.labels)):
            if self.labels[i] == -1:
                self.current_index = i
                break
        self.update_text()

    def update_text(self):
        if self.current_index >= 0 and self.current_index < len(self.texts):
            num_label = self.labels[self.current_index]
            if  num_label== -1:
                label = 'NOT LABELED'
                color = 'grey'
            elif num_label == 1:
                label = 'POSITIVE'
                color = 'red'
            elif num_label == 0:
                label = 'NEGATIVE'
                color = 'blue'
            
            text = self.texts[self.current_index]
            text = self.format_text(text)
            self.text_id.setText(f"Text: {self.current_index}")
            self.text_label.setText(label)
            self.text_label.setStyleSheet(f"color: {color}")
            self.text_left.setText(f"Left: {len(self.texts)-self.current_index-1}")
            self.text_display.setStyleSheet(f'border: 4px solid {color}')
            self.text_display.setText(text)

    def go_to_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_text()

    def go_to_next(self):
        if self.current_index < len(self.texts) - 1:
            self.current_index += 1
            self.update_text()

    def label_text(self, label):
        self.labels[self.current_index] = label
        self.update_text()
        # self.go_to_next()

    def keyPressEvent(self, event):
        text_display = self.text_display
        if event.key() == Qt.Key_Left or event.key() == Qt.Key_3:
            self.go_to_previous()
        elif event.key() == Qt.Key_Right or event.key() == Qt.Key_4:
            self.go_to_next()
        elif event.key() == Qt.Key_5:
            self.go_to_unlabeled()
        elif event.key() == Qt.Key_1:
            self.label_text(1)
        elif event.key() == Qt.Key_2:
            self.label_text(0)
        elif event.key() == Qt.Key_Down:
            scroll_bar = text_display.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.value() + 2*scroll_bar.singleStep())  # scrolling dowm
        elif event.key() == Qt.Key_Up:
            scroll_bar = text_display.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.value() - 2*scroll_bar.singleStep())  # scrolling up
        elif event.modifiers() & Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                text_display.selectAll()
            elif event.key() == Qt.Key_C:
                text_display.copy()
    
    def load_data(self):
        self.dh.load_data()
        self.texts = self.dh.texts
        self.labels = self.dh.labels
        self.current_index = 0

    def save_data(self):
        self.dh.texts = self.texts
        self.dh.labels = self.labels
        self.dh.save_data()

    def closeEvent(self, event):
        self.save_data()

if __name__ == "__main__":
    app = QApplication(argv)
    window = TextAnnotationApp()
    window.show()
    exit(app.exec_())
