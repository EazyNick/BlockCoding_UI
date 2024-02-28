import pyautogui

def Click(x, y):
    # x, y 좌표를 정수로 변환
    x = int(x)
    y = int(y)
    pyautogui.moveTo(x, y)
    # 현재 위치에서 마우스 클릭
    pyautogui.click()