import sys

if len(sys.argv) != 2:
    print("Usage: python yolo_mode_test.py <image_folder>")
    sys.exit(1)


from ultralytics import YOLO
import cv2
import os
import numpy as np


def show_text(img, text, pos):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)


image_folder = sys.argv[1]
model = YOLO("./runs/detect/train12/weights/best.pt")
image_files = [
    (os.path.join(image_folder, file), file, int(file[:-4]))
    for file in os.listdir(image_folder)
    if file.endswith(".jpg")
]
image_files.sort(key=lambda x: x[2])

for image_path, image_name, _ in image_files:
    img = cv2.imread(image_path)
    results = model.predict(image_path, conf=0.5, imgsz=640)
    show_text(img, "Press any button to show next", (50, 50))
    show_text(img, "Press 'q' to quit", (50, 100))
    if len(results[0].boxes) == 0:
        show_text(img, "No fishing float detected", (50, 150))
    else:
        show_text(img, "Fishing float detected", (50, 150))
        boxes = results[0].boxes.cpu().numpy()
        best = np.argmax(boxes.conf)
        conf = boxes.conf[best]
        cls = int(boxes.cls[best])
        x, y, w, h = boxes.xywh[best]
        x, y, w, h = int(x), int(y), int(w), int(h)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        if cls == 0:
            class_name = "fishing"
        elif cls == 1:
            class_name = "fish_bites"
        else:
            class_name = str(cls)
        show_text(img, f"{class_name}:{conf:.3f}", (x, y - 10))
    cv2.imshow("img", img)
    op = cv2.waitKey(1)
    if op == ord("q"):
        exit(0)
