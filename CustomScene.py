from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtCore import Qt

class CustomScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(CustomScene, self).__init__(parent)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            selected_items = self.selectedItems()
            if selected_items:
                for item in selected_items:
                    self.removeItem(item)
                event.accept()
            else:
                event.ignore()
        else:
            super(CustomScene, self).keyPressEvent(event)