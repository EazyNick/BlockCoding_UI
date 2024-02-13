import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QGraphicsScene, QApplication
from PyQt5.QtGui import QBrush, QColor

from custom_graphics_view import CustomGraphicsView
from node import Node

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Node-based UI in PyQt')
        self.setGeometry(100, 100, 1000, 600)
        self.nodes = []  # 생성된 노드들을 저장할 리스트
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # "실행" 버튼 추가
        execute_button = QPushButton('실행')
        execute_button.clicked.connect(self.executeNodes)
        layout.addWidget(execute_button)

        # # 노드 추가 버튼
        # add_node_button = QPushButton('Add Node')
        # add_node_button.clicked.connect(self.addNode)
        # layout.addWidget(add_node_button)

        # 추가 버튼 1
        button1 = QPushButton('Add Click')
        button1.clicked.connect(self.AddClickNode)
        layout.addWidget(button1)

        # 추가 버튼 2
        button2 = QPushButton('Add Scroll')
        button2.clicked.connect(self.AddScrollNode)
        layout.addWidget(button2)

        # 추가 버튼 3
        button3 = QPushButton('Add Command')
        button3.clicked.connect(self.AddCommandNode)
        layout.addWidget(button3)

        # 노드를 담을 그래픽스 뷰
        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self.scene)
        #self.setCentralWidget(self.view)
        # 배경 색상을 설정합니다. 예를 들어 어두운 회색 계열의 색상입니다.
        backgroundColor = QColor('#393939')  # 어두운 배경색
        self.scene.setBackgroundBrush(QBrush(backgroundColor))
        self.view.setScene(self.scene)
        self.view.setFixedSize(800, 600)
        layout.addWidget(self.view)

    def addNode(self, nodeType):
        node_name = f'{nodeType} Node {len(self.nodes) + 1}'
        node = Node(node_name, nodeType)
        self.nodes.append(node)
        self.scene.addItem(node)
        self.rearrangeNodes()

    def AddClickNode(self):
        # 버튼 1 클릭 이벤트 핸들러
        node_name = f'Click Node {len(self.nodes) + 1}'
        node = Node(node_name, "Click")
        self.nodes.append(node)

        # 뷰포트의 중앙 좌표를 계산
        viewport_center = self.view.mapToScene(self.view.viewport().rect().center())

        # 장면에 노드 추가하고 뷰포트 중앙에 배치
        self.scene.addItem(node)
        node.setPos(viewport_center.x() - node.boundingRect().width() / 2,
                    viewport_center.y() - node.boundingRect().height() / 2)
        print("Button 1 clicked")

    def AddScrollNode(self):
        node_name = f'Scroll Node {len(self.nodes) + 1}'
        node = Node(node_name, "Scroll")
        self.nodes.append(node)

        # 뷰포트의 중앙 좌표를 계산
        viewport_center = self.view.mapToScene(self.view.viewport().rect().center())

        # 장면에 노드 추가하고 뷰포트 중앙에 배치
        self.scene.addItem(node)
        node.setPos(viewport_center.x() - node.boundingRect().width() / 2,
                    viewport_center.y() - node.boundingRect().height() / 2)
        print("Button 2 clicked")

    def AddCommandNode(self):

        node_name = f'Command Node {len(self.nodes) + 1}'
        node = Node(node_name, "Command")
        self.nodes.append(node)

        # 뷰포트의 중앙 좌표를 계산
        viewport_center = self.view.mapToScene(self.view.viewport().rect().center())

        # 장면에 노드 추가하고 뷰포트 중앙에 배치
        self.scene.addItem(node)
        node.setPos(viewport_center.x() - node.boundingRect().width() / 2,
                    viewport_center.y() - node.boundingRect().height() / 2)
        
        # 버튼 3 클릭 이벤트 핸들러
        print("Button 3 clicked")

    def rearrangeNodes(self):
        # 노드를 X 좌표에 따라 정렬하고 재배치
        # 각 노드의 X 좌표(x.x())에 따라 오름차순으로 정렬
        # x.x() 메서드는 QGraphicsItem의 메서드로, 해당 아이템의 X 좌표 값을 반환
        sorted_nodes = sorted(self.nodes, key=lambda x: x.x())
        x_offset = 10
        for node in sorted_nodes:
            node.setPos(x_offset, 100)  # Y 좌표는 예시로 100으로 설정
            x_offset += 160  # 노드 간격 설정

    def executeNodes(self):
        # 노드 실행 로직
        for node in sorted(self.nodes, key=lambda x: x.x()):
            print(f'Executing {node.nodeType} node: {node.name}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())