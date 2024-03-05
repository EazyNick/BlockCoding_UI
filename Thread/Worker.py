from PyQt5.QtCore import QThread, pyqtSignal
from Logger.Logger import *

class Worker(QThread):

    finished = pyqtSignal()  # 작업 완료 신호

    def __init__(self, executeNodesFunc):
        super().__init__()
        self.executeNodesFunc = executeNodesFunc  # 실행할 함수

    def run(self):
        LOG.debug("스레드 런")
        self.executeNodesFunc()  # 함수 실행
        LOG.debug("스레드 종료")
        self.finished.emit()  # 작업 완료 시그널 발생