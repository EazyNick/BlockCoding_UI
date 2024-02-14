import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QPushButton, QGraphicsScene, QApplication, QVBoxLayout, QSplitter, QMessageBox
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt
import json

from define import *
from custom_graphics_view import CustomGraphicsView
from node import Node

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle('Node-based UI in PyQt')
        self.setGeometry(100, 100, 1000, 600)
        self.nodes = []  # 생성된 노드들을 저장할 리스트
        self.running = False  # 실행 중인지 추적하는 플래그
        self.initUI()

    def initUI(self):
        # 창을 띄울 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 메인 수평 스플리터 레이아웃
        main_splitter = QSplitter(Qt.Horizontal)
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(main_splitter)

        # 왼쪽 레이아웃 생성 (버튼들을 세로로 배열)
        left_layout = QVBoxLayout()
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        main_splitter.addWidget(left_widget)

        # 공통 스타일 시트 설정
        #button_style = "QPushButton { margin: 0; padding: 2px; }"

        # "실행" 버튼 추가
        execute_button = createButton('실행', self.executeNodes)
        left_layout.addWidget(execute_button)

        # "중단" 버튼 추가
        execute_button2 = createButton('중단', self.stopExecution)
        left_layout.addWidget(execute_button2)

        Distance(left_layout)

        # "저장하기" 버튼 추가
        execute_button4 = createButton('저장하기', self.saveNodes)
        left_layout.addWidget(execute_button4)

        # "불러오기" 버튼 추가
        execute_button3 = createButton('불러오기', self.confirmLoadNodes)
        left_layout.addWidget(execute_button3)

        Distance(left_layout)

        # 추가 버튼 1
        button1 = createButton('Add Click', self.AddClickNode)
        left_layout.addWidget(button1)

        # 추가 버튼 2
        button2 = createButton('Add Scroll', self.AddScrollNode)
        left_layout.addWidget(button2)

        # 추가 버튼 3
        button3 = createButton('Add Command', self.AddCommandNode)
        left_layout.addWidget(button3)

        # 레이아웃의 나머지 공간을 채우기 위해 스트레치 요소 추가
        left_layout.addStretch()

        # 노드를 담을 그래픽스 뷰
        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self.scene)
        #self.setCentralWidget(self.view)
        # 배경 색상을 설정합니다. 예를 들어 어두운 회색 계열의 색상입니다.
        backgroundColor = QColor('#393939')  # 어두운 배경색
        self.scene.setBackgroundBrush(QBrush(backgroundColor))
        self.view.setScene(self.scene)
        self.view.setFixedSize(800, 600)
        main_splitter.addWidget(self.view)

        # 씬에 포커스를 설정
        self.scene.setFocus()

    # def addNode(self, nodeType):
    #     node_name = f'{nodeType} Node {len(self.nodes) + 1}'
    #     node = Node(node_name, nodeType)
    #     self.nodes.append(node)
    #     self.scene.addItem(node)
    #     self.rearrangeNodes()

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
        self.running = True
        for node in sorted(self.nodes, key=lambda x: x.x()):
            if not self.running:  # 만약 실행을 중단해야 한다면 루프 탈출
                break
            for i in range(1000):
                print(f'Executing {node.nodeType} node: {node.name}')
        self.running = False

    def stopExecution(self):
        self.running = False  # 실행 중단
        # 필요한 경우 초기 상태로 되돌리는 코드 추가

    def saveNodes(self):
        nodes_data = []
        for node in self.nodes:
            node_info = {
                'name': node.name,
                'type': node.nodeType,
                'position': {'x': node.x(), 'y': node.y()}
            }
            nodes_data.append(node_info)

        with open('nodes_state.json', 'w') as file:
            json.dump(nodes_data, file)

    def loadNodes(self):

        # 기존에 노드들을 삭제
        self.scene.clear()
        self.nodes.clear()

        try:
            with open('nodes_state.json', 'r') as file:
                nodes_data = json.load(file)
                for node_data in nodes_data:
                    node = Node(node_data['name'], node_data['type'])
                    self.nodes.append(node)
                    self.scene.addItem(node)
                    node.setPos(node_data['position']['x'], node_data['position']['y'])
        except FileNotFoundError:
            print("No saved state found.")

    def confirmLoadNodes(self):
        if self.nodes:  # 이미 노드가 하나 이상 있는 경우
            reply = QMessageBox.question(self, '노드 불러오기',
                                         "노드를 불러올 시, 현재 진행한 내역들이 모두 사라집니다. 계속하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.loadNodes()  # 노드 불러오기
            else:
                print("불러오기 취소됨")  # 콘솔에 메시지 출력
        else:
            self.loadNodes()  # 노드가 없으므로 바로 불러오기

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())