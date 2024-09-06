import numpy as np
from window_capture import WindowCapture
import win32gui, win32con, win32api
import random
import time
import math


# Press '4' which is my big fishing float hotkey
def use_big_fishing_float():
    win32api.keybd_event(0x34, 0, 0, 0)
    time.sleep(0.1 + 0.1 * random.random())
    win32api.keybd_event(0x34, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(5)


def mouse_right_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.1 + 0.1 * random.random())
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)


# Press Alt + ` which is my fish hotkey
def retry_keybd():
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    time.sleep(0.1 + 0.1 * random.random())
    win32api.keybd_event(0xC0, 0, 0, 0)
    time.sleep(0.2 + 0.2 * random.random())
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.1 + 0.1 * random.random())
    win32api.keybd_event(0xC0, 0, win32con.KEYEVENTF_KEYUP, 0)


# Press Alt + Tab to switch back
def switch_back():
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    time.sleep(0.02 + 0.02 * random.random())
    win32api.keybd_event(win32con.VK_TAB, 0, 0, 0)
    time.sleep(0.02 + 0.02 * random.random())
    win32api.keybd_event(win32con.VK_TAB, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.02 + 0.02 * random.random())
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)


def mouse_move(x, y, r=20):
    c_x, c_y = win32api.GetCursorPos()
    dist_x = x - c_x
    dist_y = y - c_y
    dist = math.sqrt(dist_x * dist_x + dist_y * dist_y)
    if dist == 0:
        return
    dir_x = dist_x / dist
    dir_y = dist_y / dist
    while True:
        c_x, c_y = win32api.GetCursorPos()
        dist_x = x - c_x
        dist_y = y - c_y
        dist = math.sqrt(dist_x * dist_x + dist_y * dist_y)
        if dist == 0:
            break
        dir_x = dist_x / dist
        dir_y = dist_y / dist
        if dist < r:
            break
        if dist > 100:
            delta = random.randint(40, 60)
        elif dist > 50:
            delta = random.randint(20, 40)
        else:
            delta = random.randint(10, 20)
        win32api.mouse_event(
            win32con.MOUSEEVENTF_MOVE, int(dir_x * delta), int(dir_y * delta), 0, 0
        )
        time.sleep(0.02 + 0.01 * random.random())


hwnd = win32gui.FindWindow(None, "魔兽世界")
if hwnd == 0:
    print("窗口未找到")
    exit(0)
else:
    from ultralytics import YOLO

    model = YOLO("./runs/detect/train12/weights/best.pt")

    print(f"窗口句柄:{hwnd}")
    try:
        window_capture = WindowCapture(hwnd)
        window_left = window_capture.left
        window_top = window_capture.top
        not_fishing_count = 0
        fish_bites_count = 0
        start_time = 0
        while True:
            if time.time() - start_time > 30 * 60:
                use_big_fishing_float()
                start_time = time.time()
            img = window_capture.capture()
            results = model.predict(img, conf=0.5, imgsz=640, verbose=False)
            if len(results[0].boxes) == 0:
                print("Not fishing")
                not_fishing_count += 1
                if not_fishing_count < 10:
                    continue
                not_fishing_count = 0
                x = int(window_left + window_capture.width * 0.5)
                y = int(window_top + window_capture.height * 0.5)
                mouse_move(x, y, 50)
                time.sleep(0.2 + random.random() * 0.2)
                mouse_right_click()
                time.sleep(0.2 + random.random() * 0.2)
                retry_keybd()
                time.sleep(0.1 + random.random() * 0.1)
                switch_back()
                time.sleep(2 + random.random() * 0.5)
            else:
                boxes = results[0].boxes.cpu().numpy()
                best = np.argmax(boxes.conf)
                conf = boxes.conf[best]
                cls = int(boxes.cls[best])
                x, y, w, h = boxes.xywh[best]
                x, y, w, h = int(x), int(y), int(w), int(h)
                if cls == 0:
                    print(f"Fishing [{conf:0.3f}]")
                elif cls == 1:
                    print(f"Fish bites [{conf:0.3f}]")
                    if conf > 0.8:
                        fish_bites_count += 1
                    if fish_bites_count < 3:
                        continue
                    fish_bites_count = 0
                    mouse_x = int(window_left + x + w * 0.5)
                    mouse_y = int(window_top + y + h * 0.5)
                    mouse_move(mouse_x, mouse_y)
                    time.sleep(0.03 + random.random() * 0.01)
                    mouse_right_click()
                    time.sleep(0.5 + random.random() * 0.5)
                    retry_keybd()
                    time.sleep(0.1 + random.random() * 0.1)
                    switch_back()
                    time.sleep(2 + random.random() * 0.5)
                else:
                    print(f"unknown cls:{cls} [{conf:0.3f}]")
    except KeyboardInterrupt as e:
        exit(0)
