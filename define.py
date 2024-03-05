from PyQt5.QtWidgets import QSpacerItem, QSizePolicy, QPushButton

def Distance(layout):
    # 버튼 사이의 작은 간격 추가
    spacer = QSpacerItem(0, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout.addItem(spacer)

def createButton(title, callback):
        """
        버튼을 생성하고 설정하는 메서드입니다.

        :param title: 버튼에 표시될 텍스트입니다.
        :param callback: 버튼이 클릭되었을 때 호출될 함수입니다.
        :return: 생성된 QPushButton 객체입니다.
        """

        # button_style = "QPushButton { margin: 0; padding: 2px; }"
        # button.setStyleSheet(button_style)

        button = QPushButton(title)
        button.clicked.connect(callback)

        return button