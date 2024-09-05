import cv2
import numpy as np
from window_capture import WindowCapture
import win32gui
import threading


def show_text(img, text, pos):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)


hwnd = win32gui.FindWindow(None, "魔兽世界")
if hwnd == 0:
    print("窗口未找到")
    exit(0)
else:
    from ultralytics import YOLO

    model = YOLO("./runs/detect/train15/weights/best.pt")

    print(f"窗口句柄:{hwnd}")
    window_capture = WindowCapture(hwnd)
    while True:
        img = window_capture.capture()
        results = model.predict(img, conf=0.5, imgsz=640)
        show_text(img, "Press 'q' to quit", (50, 100))
        if len(results[0].boxes) == 0:
            show_text(img, "No fishing float detected", (50, 150))
        else:
            show_text(img, "Fishing float detected", (50, 150))
            boxes = results[0].boxes.cpu().numpy()
            best = np.argmax(boxes.conf)
            conf = boxes.conf[best]
            x, y, w, h = boxes.xywh[best]
            x, y, w, h = int(x), int(y), int(w), int(h)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            show_text(img, f"{conf:.3f}", (x, y - 10))
        cv2.imshow("img", img)
        op = cv2.waitKey(1)
        if op == ord("q"):
            exit(0)
