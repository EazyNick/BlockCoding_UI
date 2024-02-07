import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGraphicsItemGroup, 
                            QGraphicsTextItem, QGraphicsRectItem, QGraphicsScene, 
                            QGraphicsView, QPushButton, QHBoxLayout, QGraphicsItem)
from PyQt5.QtGui import QBrush, QColor, QPen

class Node(QGraphicsItemGroup):
    """
    Node 클래스
    QGraphicsItemGroup을 상속
    여러 그래픽스(QGraphicsItem 클래스의 인스턴스) 아이템을 그룹화할 수 있게 해줍니다.
    즉, 각 아이템이 독립적으로 동작 하는데, 이를 그룹화 한 것
    """

    def __init__(self, name):
        super().__init__()  # 기반 클래스(QGraphicsItemGroup)의 생성자를 호출
        self.name = name  # 노드의 이름을 인스턴스 변수에 저장, Node(name)
        self.initUI()  # UI를 초기화하는 사용자 정의 메서드 호출

    def initUI(self):
        # 노드 블록의 색상을 설정합니다. 예를 들어 어두운 빨강색과 어두운 파란색 등입니다.
        nodeColor = QColor('#7f0000')  # 어두운 빨강색
        borderColor = QColor('#2f2f2f')  # 경계선 색상

        rect = QGraphicsRectItem(0, 0, 150, 50)  # 150x50 크기의 직사각형 아이템을 생성
        rect.setBrush(QBrush(nodeColor)) # 노드 블록 색상
        rect.setPen(QPen(borderColor)) # 노드 블록 경계선 색상
        text = QGraphicsTextItem(self.name, self)  # 노드 이름을 표시할 텍스트 아이템을 생성, self(QGraphicsTextItem의 부모노드를 Node 클래스로 정의)
        text.setDefaultTextColor(QColor(255, 255, 255))  # 흰색으로 텍스트 색상 설정
        text.setPos(5, 5)  # 텍스트 아이템의 위치를 설정
        text.setZValue(1)  # 다른 아이템보다 더 높은 Z-Order 값을 설정

        # 노드가 드래그 가능하도록 설정
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.addToGroup(rect)  # 직사각형 아이템을 이 그룹에 추가합니다.
        self.addToGroup(text)  # 텍스트 아이템을 이 그룹에 추가합니다.

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Node-based UI in PyQt')
        self.setGeometry(100, 100, 1000, 600)

        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        # 노드 추가 버튼
        add_node_button = QPushButton('Add Node')
        add_node_button.clicked.connect(self.addNode)
        layout.addWidget(add_node_button)

        # 노드를 담을 그래픽스 뷰
        self.view = QGraphicsView()
        self.scene = QGraphicsScene()
        # 배경 색상을 설정합니다. 예를 들어 어두운 회색 계열의 색상입니다.
        backgroundColor = QColor('#393939')  # 어두운 배경색
        self.scene.setBackgroundBrush(QBrush(backgroundColor))
        self.view.setScene(self.scene)
        self.view.setFixedSize(800, 600)
        layout.addWidget(self.view)

        # 노드들을 담을 리스트
        self.nodes = []

    def addNode(self):
        # 새 노드 생성
        node_name = f'Node {len(self.nodes) + 1}'
        node = Node(node_name)
        self.nodes.append(node)

        # 뷰포트의 중앙 좌표를 계산
        viewport_center = self.view.mapToScene(self.view.viewport().rect().center())

        # 장면에 노드 추가하고 뷰포트 중앙에 배치
        self.scene.addItem(node)
        node.setPos(viewport_center.x() - node.boundingRect().width() / 2,
                    viewport_center.y() - node.boundingRect().height() / 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())