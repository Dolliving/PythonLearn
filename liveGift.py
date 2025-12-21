# 坐标获取工具
import pyautogui
import time

print("将鼠标移动到检测区域的左上角，等待5秒...")
time.sleep(5)
x1, y1 = pyautogui.position()
print(f"左上角坐标: ({x1}, {y1})")

print("将鼠标移动到检测区域的右下角，等待5秒...")
time.sleep(5)
x2, y2 = pyautogui.position()
print(f"右下角坐标: ({x2}, {y2})")

width = x2 - x1
height = y2 - y1
print(f"检测区域: ({x1}, {y1}, {width}, {height})")