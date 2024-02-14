from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import QPoint, Qt

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setDragMode(QGraphicsView.NoDrag)
        self.dragging = False
        self.lastMousePosition = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton and self.sceneRect().contains(self.mapToScene(event.pos())):
            self.dragging = True
            self.lastMousePosition = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.lastMousePosition
            self.lastMousePosition = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.dragging = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         # 여기서 추가적인 로직이 있다면, 필요한 경우 부모의 mousePressEvent를 호출해야 함
    #         super().mousePressEvent(event)
