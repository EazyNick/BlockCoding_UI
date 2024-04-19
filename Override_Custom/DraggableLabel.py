from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super(DraggableLabel, self).__init__(parent)
        self.setFixedSize(100, 100)
        self.setStyleSheet("background-color: blue; border: 1px solid black;")
        self.setMouseTracking(True)
        self.dragging = False   

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.mouse_start_point = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToParent(event.pos() - self.mouse_start_point))
            self.parent().check_snap(self)

    def mouseReleaseEvent(self, event):
        self.dragging = False