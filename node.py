from PyQt5.QtWidgets import QGraphicsItemGroup, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem, QLineEdit, QGraphicsProxyWidget 
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QBrush, QColor, QPen, QIntValidator, QRegExpValidator

class Node(QGraphicsItemGroup):
    """
    Node 클래스
    QGraphicsItemGroup을 상속
    여러 그래픽스(QGraphicsItem 클래스의 인스턴스) 아이템을 그룹화할 수 있게 해줍니다.
    즉, 각 아이템이 독립적으로 동작 하는데, 이를 그룹화 한 것
    """

    def __init__(self, name, nodeType):
        super().__init__()  # 기반 클래스(QGraphicsItemGroup)의 생성자를 호출
        self.name = name  # 노드의 이름을 인스턴스 변수에 저장, Node(name)
        self.nodeType = nodeType  # 노드 유형 추가
        self.initUI()  # UI를 초기화하는 사용자 정의 메서드 호출

    def initUI(self):
        # 노드 블록의 색상을 설정합니다. 예를 들어 어두운 빨강색과 어두운 파란색 등입니다.
        nodeColor = QColor('#7f0000')  # 어두운 빨강색
        borderColor = QColor('#2f2f2f')  # 경계선 색상

        # QLineEdit 추가
        if self.nodeType == "Click":
            self.lineEdit = QLineEdit()
            # 입력 길이 제한 (예시: 10자리까지)
            self.lineEdit.setMaxLength(10)
            proxyWidget = QGraphicsProxyWidget(self)  # QGraphicsScene에서 위젯 사용을 위한 프록시
            proxyWidget.setWidget(self.lineEdit)
            proxyWidget.setPos(5, 60)  # QLineEdit 위치 조정

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

    def mousePressEvent(self, event):
    # 이벤트를 상위 클래스에 전달하여 기본적인 이벤트 처리를 수행하게 합니다.
        super().mousePressEvent(event)