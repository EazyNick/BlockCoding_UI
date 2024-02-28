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

    def keyPressEvent(self, event):
        # 현재 포커스가 있는 아이템이 키 이벤트를 처리할 수 있도록 합니다.
        if self.scene().focusItem():
            self.scene().focusItem().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

