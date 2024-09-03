from window_capture import WindowCapture
import cv2
import win32gui
import threading
import time
from datetime import datetime
import os


def capture_thread():
    global is_catpure
    is_catpure = True
    folder_name = "./data/origin_data/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    print(f"开始截图，保存到{folder_name}文件夹")
    count = 0
    while is_catpure:
        img = window_capture.capture()
        time.sleep(0.1)
        count += 1
        cv2.imwrite(f"{folder_name}/{count}.jpg", img)
        print(f"\r[{count}] 请输入指令(r:开始新一轮截图，q:退出):", end="")
    print()


hwnd = win32gui.FindWindow(None, "魔兽世界")
if hwnd == 0:
    print("窗口未找到")
    exit(0)
else:
    print(f"窗口句柄:{hwnd}")
    window_capture = WindowCapture(hwnd)

    is_catpure = False
    task = None
    op = input("请输入指令(r:开始新一轮截图，q:退出):")
    while True:
        if op == "r":
            is_catpure = False
            if task and task.is_alive():
                task.join()
            task = threading.Thread(target=capture_thread)
            task.start()
        elif op == "q":
            is_catpure = False
            if task and task.is_alive():
                task.join()
            break
        else:
            print("无效操作\n")
            print("请输入指令(r:开始新一轮截图，q:退出):", end="")
        op = input()
