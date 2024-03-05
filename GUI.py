import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QSplitter, QMessageBox
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import json
import os
import threading

from Thread.Worker import Worker
from Logger.Logger import *
from SaveAction.SaveJson import save_json
from Execute_Def.Click import Click
from Execute_Def.Scroll import Scroll
#from Execute_Def.Command import Command
from Override_Custom.CustomScene import CustomScene
from define import *
from Override_Custom.custom_graphics_view import CustomGraphicsView
from node import Node

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle('Node-based UI in PyQt')
        self.setGeometry(100, 100, 1000, 600)
        self.nodes = []  # 생성된 노드들을 저장할 리스트
        self.x = []  # x 좌표를 저장할 리스트
        self.y = []  # y 좌표를 저장할 리스트
        self.running = False  # 실행 중인지 추적하는 플래그
        self.worker = Worker(self.executeNodes())  # 백그라운드 작업을 위한 Worker 인스턴스
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
        execute_button = QPushButton('실행', self)
        execute_button.clicked.connect(self.startWork)
        left_layout.addWidget(execute_button)

        # "중단" 버튼 추가
        execute_button2 = QPushButton('중단', self)
        execute_button2.clicked.connect(self.stopWork)
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
        # CustomScene 인스턴스 생성
        self.scene = CustomScene()
        self.view = CustomGraphicsView(self.scene)
        #self.setCentralWidget(self.view)
        # 배경 색상을 설정합니다. 예를 들어 어두운 회색 계열의 색상입니다.
        backgroundColor = QColor('#393939')  # 어두운 배경색
        self.scene.setBackgroundBrush(QBrush(backgroundColor))
        self.view.setScene(self.scene)
        self.view.setFixedSize(800, 600)
        main_splitter.addWidget(self.view)

    def startWork(self):
        if not self.worker.isRunning():  # 작업이 이미 실행 중이지 않은 경우에만 시작
            self.worker = Worker(self.executeNodes)  # Worker 인스턴스 생성
            self.worker.finished.connect(self.stopWork)  # 작업 완료 시 처리할 슬롯 연결
            self.worker.start()  # Worker 스레드 시작

    def stopWork(self):
        if self.worker.isRunning():
            self.stopExecution()
            self.worker.terminate()  # Worker 스레드 종료 (주의: terminate는 강제 종료이므로 리소스 정리가 필요할 수 있음)

    def handleCoordinates(self, node_index, x = [], y = []):
        # 리스트의 길이를 검사하여 새 노드 인덱스가 리스트 범위 내에 있는지 확인합니다.
        # node_index는 노드의 인덱스를 나타내며, 0부터 시작합니다.
        if node_index >= len(self.x):
            # 리스트를 확장합니다.
            self.x.append(x)
            self.y.append(y)
        else:
            # 이미 존재하는 인덱스라면 값을 업데이트합니다.
            self.x[node_index] = x
            self.y[node_index] = y
        
        print(f"Received coordinates for node {node_index + 1}: ({self.x[node_index]}, {self.y[node_index]})")

    def AddClickNode(self):
        # 버튼 1 클릭 이벤트 핸들러
        node_index = len(self.nodes)  # 현재 노드 인덱스
        node_name = f'Click Node {len(self.nodes) + 1}'
        node = Node(self.scene, node_name, "Click", 100, 100, self.handleCoordinates(node_index))
        self.nodes.append(node)

        # 뷰포트의 중앙 좌표를 계산
        viewport_center = self.view.mapToScene(self.view.viewport().rect().center())

        # 장면에 노드 추가하고 뷰포트 중앙에 배치
        self.scene.addItem(node)
        # Node 인스턴스를 생성하고 콜백 함수를 전달합니다.
        node.setPos(viewport_center.x() - node.boundingRect().width() / 2,
                    viewport_center.y() - node.boundingRect().height() / 2)
        
    def AddScrollNode(self):
        node_name = f'Scroll Node {len(self.nodes) + 1}'
        node = Node(self.scene, node_name, "Scroll", 100, 100)
        self.nodes.append(node)

        # 뷰포트의 중앙 좌표를 계산
        viewport_center = self.view.mapToScene(self.view.viewport().rect().center())

        # 장면에 노드 추가하고 뷰포트 중앙에 배치
        self.scene.addItem(node)
        node.setPos(viewport_center.x() - node.boundingRect().width() / 2,
                    viewport_center.y() - node.boundingRect().height() / 2)
        LOG.info("Button 2 clicked")

    def AddCommandNode(self):

        node_name = f'Command Node {len(self.nodes) + 1}'
        node = Node(self.scene, node_name, "Command", 100, 100, self.handleCoordinates)
        self.nodes.append(node)

        # 뷰포트의 중앙 좌표를 계산
        viewport_center = self.view.mapToScene(self.view.viewport().rect().center())

        # 장면에 노드 추가하고 뷰포트 중앙에 배치
        self.scene.addItem(node)
        node.setPos(viewport_center.x() - node.boundingRect().width() / 2,
                    viewport_center.y() - node.boundingRect().height() / 2)
        
        # 버튼 3 클릭 이벤트 핸들러
        LOG.info("Button 3 clicked")

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
        LOG.debug(f"self.nodes: {self.nodes}")
        # self.running이 True인 동안 작업을 계속 실행

        try:
            LOG.info(f"노드 실행중")
        # 노드를 x 좌표에 따라 정렬합니다.
            sorted_nodes = sorted(self.nodes, key=lambda item: item.x)
            LOG.debug(f"sorted_nodes: {sorted_nodes}")
            for node in sorted_nodes:
                x = node.x
                y = node.y
                delay = node.delay

                # x, y, delay 값이 설정되지 않은 경우 로그를 남깁니다.
                if -1 in [x, y, delay]: 
                    LOG.info(f"{node.name} 노드의 x, y, delay 값이 설정되지 않았습니다.")
                    continue  # 다음 노드로 넘어갑니다.

                # 노드 타입에 따라 적절한 작업을 수행합니다.
                LOG.info(f"Node {node.name}: delay = {delay}, x = {x}, y = {y}")
                if node.nodeType == "Click":
                    Click(x, y, delay)
                    LOG.info(f'Executing {node.nodeType} node: {node.name}')

                elif node.nodeType == "Scroll":
                    Scroll(x, y, delay)
                    LOG.info(f"Scroll Test for {node.name}")

                elif node.nodeType == "Command":
                    # Command(x, y, delay)  # Command에 해당하는 작업을 수행해야 합니다.
                    LOG.info(f"Command Test for {node.name}")
            threading.sleep(1)  # 실제 구현에서는 sleep을 사용하지 않습니다.
            
        except:
            # 'delay' 속성이 없을 경우 실행됩니다.
            print("Error: 'x' or 'y' or 'delay' attribute not found. Using default delay value.")
            # 기본 delay 값을 사용하거나, 다른 처리를 할 수 있습니다.
            x = -1
            y = -1
            delay = -1 
            # 여기에서 default_delay를 사용한 처리를 계속할 수 있습니다.          
        self.running = False
        self.thread = None
        LOG.debug("노드 실행 완료")

    def stopExecution(self):
        # 실행 중단 플래그 설정
        self.running = False
        # 스레드가 실행 중이면, 스레드가 종료될 때까지 기다림
        if self.thread is not None:
            self.thread.join()
            self.thread = None

    def saveNodes(self):
        nodes_data = []
        for node in self.nodes:
            x = node.pos().x()
            y = node.pos().y()
            # QLineEdit의 텍스트도 저장합니다.
            text = node.lineEdit.text() if hasattr(node, 'lineEdit') else ""
            node_info = {
                'name': node.name,
                'type': node.nodeType,
                'position': {'x': x, 'y': y},
                'text': text  # QLineEdit의 텍스트를 저장합니다.
            }
            nodes_data.append(node_info)

        save_json(nodes_data)

    def loadNodes(self):
        self.scene.clear()
        self.nodes.clear()

        filepath = os.path.join('Data', 'nodes_state.json')

        try:
            with open(filepath, 'r') as file:
                nodes_data = json.load(file)
                for node_data in nodes_data:
                    node = Node(self.scene, node_data['name'], node_data['type'], 
                                node_data['position']['x'], node_data['position']['y'])
                    self.nodes.append(node)
                    self.scene.addItem(node)
                    node.setPos(node_data['position']['x'], node_data['position']['y'])

                    # 저장된 텍스트 값을 QLineEdit에 다시 설정합니다.
                    if hasattr(node, 'lineEdit'):
                        node.lineEdit.setText(node_data.get('text', ""))

        except FileNotFoundError:
            LOG.info("No saved state found.")

    def confirmLoadNodes(self):
        if self.nodes:  # 이미 노드가 하나 이상 있는 경우
            reply = QMessageBox.question(self, '노드 불러오기',
                                         "노드를 불러올 시, 현재 진행한 내역들이 모두 사라집니다. 계속하시겠습니까?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.loadNodes()  # 노드 불러오기
            else:
                LOG.info("불러오기 취소됨")  # 콘솔에 메시지 출력
        else:
            self.loadNodes()  # 노드가 없으므로 바로 불러오기

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())