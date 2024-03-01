from PyQt5.QtWidgets import (QGraphicsItemGroup, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem, 
                             QLineEdit, QGraphicsProxyWidget, QApplication, QGraphicsScene, QMessageBox)

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QBrush, QColor, QPen
from Logger.Logger import *
class Node(QGraphicsItemGroup):
    """
    Node 클래스
    QGraphicsItemGroup을 상속
    여러 그래픽스(QGraphicsItem 클래스의 인스턴스) 아이템을 그룹화할 수 있게 해줍니다.
    즉, 각 아이템이 독립적으로 동작 하는데, 이를 그룹화 한 것
    """

    # 사용자가 입력한 x, y 값에 대한 시그널을 정의합니다.
    coordinatesEntered = pyqtSignal(int, int)

    def __init__(self, scene, name, nodeType, x, y, callback=None):
        super().__init__()  # 기반 클래스(QGraphicsItemGroup)의 생성자를 호출
        self.scene = scene
        self.name = name  # 노드의 이름을 인스턴스 변수에 저장, Node(name)
        self.nodeType = nodeType  # 노드 유형 추가
        self.x = x
        self.y = y
        self.delay = None  # 인스턴스 변수로 delay 관리
        self.callback = callback
        self.initUI()  # UI를 초기화하는 사용자 정의 메서드 호출

    def initUI(self):

        # 노드 블록의 크기를 정의합니다. 예를 들어 가로 150, 세로 100.
        nodeWidth = 150
        nodeHeight = 100  # 노드의 높이를 변경하십시오.

        # 노드 블록의 색상을 설정합니다. 예를 들어 어두운 빨강색과 어두운 파란색 등입니다.
        nodeColor = QColor('#7f0000')  # 어두운 빨강색
        borderColor = QColor('#2f2f2f')  # 경계선 색상

        # QLineEdit 추가
        if self.nodeType == "Click":
            self.lineEdit = QLineEdit()
            self.lineEdit.setPlaceholderText("Enter coordinates (x, y, delay)")
            self.proxyWidget = QGraphicsProxyWidget(self)
            self.proxyWidget.setWidget(self.lineEdit)
            self.proxyWidget.setPos(0, nodeHeight)
            
            # QLineEdit의 returnPressed 시그널을 connect 합니다.
            self.lineEdit.returnPressed.connect(self.onReturnPressed)

            self.addToGroup(self.proxyWidget)  # QLineEdit이 포함된 proxyWidget을 그룹에 추가합니다.

        if self.nodeType == "Scroll":
            self.lineEdit = QLineEdit()
            self.lineEdit.setPlaceholderText("Enter coordinates for Scroll (x, y)")
            self.proxyWidget = QGraphicsProxyWidget(self)
            self.proxyWidget.setWidget(self.lineEdit)
            self.proxyWidget.setPos(0, nodeHeight)
            
            # QLineEdit의 returnPressed 시그널을 connect 합니다.
            self.lineEdit.returnPressed.connect(self.onReturnPressed)

            self.addToGroup(self.proxyWidget)  # QLineEdit이 포함된 proxyWidget을 그룹에 추가합니다.

        if self.nodeType == "Command":
            self.lineEdit = QLineEdit()
            self.lineEdit.setPlaceholderText("Enter Command")
            self.proxyWidget = QGraphicsProxyWidget(self)
            self.proxyWidget.setWidget(self.lineEdit)
            self.proxyWidget.setPos(0, nodeHeight)
            
            # QLineEdit의 returnPressed 시그널을 connect 합니다.
            self.lineEdit.returnPressed.connect(self.onReturnPressed)

            self.addToGroup(self.proxyWidget)  # QLineEdit이 포함된 proxyWidget을 그룹에 추가합니다.

        rect = QGraphicsRectItem(0, 0, nodeWidth, nodeHeight)  # 150x50 크기의 직사각형 아이템을 생성
        rect.setBrush(QBrush(nodeColor)) # 노드 블록 색상
        rect.setPen(QPen(borderColor)) # 노드 블록 경계선 색상
        text = QGraphicsTextItem(self.name, self)  # 노드 이름을 표시할 텍스트 아이템을 생성, self(QGraphicsTextItem의 부모노드를 Node 클래스로 정의)
        text.setDefaultTextColor(QColor(255, 255, 255))  # 흰색으로 텍스트 색상 설정
        text.setPos(5, 5)  # 텍스트 아이템의 위치를 설정
        text.setZValue(1)  # 다른 아이템보다 더 높은 Z-Order 값을 설정

        # 선택 가능하도록 설정
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)

        # 노드가 드래그 가능하도록 설정
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.addToGroup(rect)  # 직사각형 아이템을 이 그룹에 추가합니다.
        self.addToGroup(text)  # 텍스트 아이템을 이 그룹에 추가합니다.

    def onReturnPressed(self):
        text = self.lineEdit.text()
        try:
            x, y, delay = map(int, text.split(','))
            self.handleCoordinates(x, y, delay)
            print("Set CallBack Def")
                
        except ValueError as e:
            print(f"Invalid input {text}: {e}")

    def handleCoordinates(self, x=None, y=None, delay=None):
        try:
            # 입력 값 검증
            if None in [x, y, delay]:
                x = -1
                y = -1
                delay = -1
                raise ValueError("x, y, and delay must not be None.")
            
            # 입력 값이 숫자인지 확인
            x = float(x)
            y = float(y)
            delay = float(delay)

            # Node로부터 전달받은 x, y 좌표와 delay를 저장합니다.
            self.x = x
            self.y = y
            self.delay = delay
            LOG.info(f"Received coordinates: ({self.x}, {self.y}, delay: {self.delay})")

        except ValueError as e:
            # 예외 메시지를 사용자에게 표시
            LOG.info(f"Error: {e}")
            # 여기에서 추가적인 오류 처리를 할 수 있습니다.
            # 예를 들어, 기본값 설정, 사용자에게 재입력 요청 등

        LOG.info(f"Received coordinates: ({self.x}, {self.y}, delay: {delay})")

    # def onReturnPressed(self):
    #     # 사용자 입력을 가져옵니다.
    #     text = self.lineEdit.text()
    #     try:
    #         # 입력 문자열을 파싱하여 x, y 좌표를 추출합니다.
    #         x, y = map(int, text.split(','))
    #         # Click 함수를 호출합니다.
    #         self.Click(x, y)
    #     except ValueError:
    #         # 입력이 잘못된 경우 에러 메시지를 출력하거나 사용자에게 알립니다.
    #         print("Invalid input. Please enter in format 'x, y'.")
            
    #         # QLineEdit의 returnPressed 시그널을 connect 합니다.
    #         self.lineEdit.returnPressed.connect(self.onReturnPressed)