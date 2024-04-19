from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QPoint
import sys
import math
from DraggableLabel import *

class SnapWidget(QWidget):
    def __init__(self):
        super(SnapWidget, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 280, 270)
        self.setWindowTitle('자석처럼 달라붙는 노드')
        self.labels = [DraggableLabel(self) for _ in range(4)]
        positions = [QPoint(10, 10), QPoint(120, 10), QPoint(10, 120), QPoint(120, 120)]
        for label, pos in zip(self.labels, positions):
            label.move(pos)

    def check_snap(self, moved_label):
        snap_threshold = 20  # 픽셀 단위
        for label in self.labels:
            if label == moved_label:
                continue
            for corner1 in self.get_corners(moved_label):
                for corner2 in self.get_corners(label):
                    if math.hypot(corner2.x() - corner1.x(), corner2.y() - corner1.y()) < snap_threshold:
                        moved_label.move(corner2.x() - (corner1.x() - moved_label.x()), corner2.y() - (corner1.y() - moved_label.y()))
                        return  # 하나의 코너에만 달라붙도록 설정

    def get_corners(self, label):
        return [label.pos(), QPoint(label.x() + label.width(), label.y()), 
                QPoint(label.x(), label.y() + label.height()), 
                QPoint(label.x() + label.width(), label.y() + label.height())]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SnapWidget()
    ex.show()
    sys.exit(app.exec_())