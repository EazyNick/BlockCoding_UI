import time
import pyautogui

def Scroll(start_pos, end_pos, delay = 2, duration=1):
    """
    start_pos: 드래그 시작 위치 (x, y)
    end_pos: 드래그 끝 위치 (x, y)
    duration: 드래그하는 데 걸리는 시간 (초)
    """
    # 시작 위치로 마우스 이동
    pyautogui.moveTo(start_pos[0], start_pos[1], duration=0.5)
    
    # 마우스를 누른 상태로 유지
    pyautogui.mouseDown()
    
    # 끝 위치로 드래그
    pyautogui.moveTo(end_pos[0], end_pos[1], duration=duration)
    
    # 마우스 버튼을 놓음
    pyautogui.mouseUp()

    time.sleep(delay)
