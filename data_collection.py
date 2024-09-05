from window_capture import WindowCapture
import cv2
import win32gui
import threading
import os

data_root = "./origin_data"


def capture_thread():
    global is_catpure
    is_catpure = True
    folder_name = os.path.join(data_root, str(len(os.listdir(data_root))))
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    print(f"开始截图，保存到{folder_name}文件夹")
    count = 0
    while is_catpure:
        img = window_capture.capture()
        count += 1
        cv2.imwrite(f"{folder_name}/{count}.jpg", img)
        print(f"\r[{count}] 输入q退出:", end="")
    print()


hwnd = win32gui.FindWindow(None, "魔兽世界")
if hwnd == 0:
    print("窗口未找到")
    exit(0)
else:
    os.makedirs(data_root, exist_ok=True)
    print(f"窗口句柄:{hwnd}")
    window_capture = WindowCapture(hwnd)
    is_catpure = False
    task = None
    task = threading.Thread(target=capture_thread)
    task.start()
    while True:
        op = input()
        if op == "q":
            is_catpure = False
            if task and task.is_alive():
                task.join()
            break
        else:
            print("无效操作\n")
