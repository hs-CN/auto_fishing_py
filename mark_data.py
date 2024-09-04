import cv2
import sys
import os


def show_text(img, text, pos):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)


if len(sys.argv) != 2:
    print("Usage: python mark_data.py <image_folder>")
    sys.exit(1)

image_folder = sys.argv[1]
img_files = [
    (os.path.join(image_folder, file_name), file_name, int(file_name[:-4]))
    for file_name in os.listdir(image_folder)
    if file_name.endswith(".jpg")
]
img_files.sort(key=lambda x: x[2])

data_mark = {}
mark_file = os.path.join(image_folder, "mark.csv")
if os.path.exists(mark_file):
    with open(mark_file, "r") as f:
        data_mark = {}
        for line in f:
            [img_path, id, x, y, w, h] = line.strip().split(",")
            data_mark[img_path] = (int(id), int(x), int(y), int(w), int(h))

roi = None
roi_confirmed = False
if len(data_mark) > 0:
    roi = data_mark[img_files[0][0]][1:]

while roi is None or not roi_confirmed:
    while roi is None:
        for img_path, img_name, img_id in img_files:
            _img = cv2.imread(img_path)
            img = _img.copy()
            show_text(img, img_name, (50, 50))
            show_text(img, "Press 's' to select ROI", (50, 100))
            show_text(img, "Press 'q' to quit", (50, 200))
            show_text(img, "Press any other to show next", (50, 150))
            cv2.imshow("img", img)
            op = cv2.waitKey(0)
            if op == ord("q"):
                exit(0)
            elif op == ord("s"):
                img = _img.copy()
                cv2.imshow("img", img)
                roi = cv2.selectROI("img", img, showCrosshair=False)
                break
    while roi is not None and not roi_confirmed:
        for img_path, img_name, img_id in img_files:
            _img = cv2.imread(img_path)
            img = _img.copy()
            show_text(img, img_name, (50, 50))
            show_text(img, "Press 's' to reselect ROI", (50, 100))
            show_text(img, "Press 'y' to confirmed ROI", (50, 150))
            show_text(img, "Press 'q' to quit", (50, 200))
            x, y, w, h = roi
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.imshow("img", img)
            op = cv2.waitKey(1)
            if op == ord("q"):
                exit(0)
            elif op == ord("s"):
                roi = None
                break
            elif op == ord("y"):
                roi_confirmed = True
                break

x, y, w, h = roi
for img_path, img_name, img_id in img_files:
    has_id = False
    while not has_id:
        img = cv2.imread(img_path)
        show_text(img, img_name, (50, 50))
        show_text(img, "Press 'q' to quit", (50, 100))
        show_text(img, "select class name:", (50, 150))
        show_text(img, "1: not fishing", (50, 200))
        show_text(img, "2: fishing", (50, 250))
        show_text(img, "3: fish", (50, 300))

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if img_path in data_mark:
            id, _, _, _, _ = data_mark[img_path]
            if id == 1:
                class_name = "not fishing"
                has_id = True
            elif id == 2:
                class_name = "fishing"
                has_id = True
            elif id == 3:
                class_name = "fish"
                has_id = True
            else:
                class_name = f"unknown class id:{id}"
            show_text(img, "Press any button to show next", (50, 350))
            show_text(img, class_name, (x + 10, y + 10))

        cv2.imshow("img", img)
        op = cv2.waitKey(0)
        if op == ord("q"):
            exit(0)
        elif op == ord("1") or op == ord("2") or op == ord("3"):
            id = 0
            if op == ord("1"):
                id = 1
            elif op == ord("2"):
                id = 2
            elif op == ord("3"):
                id = 3
            if id != 0:
                data_mark[img_path] = (id, x, y, w, h)
                has_id = True

cv2.destroyAllWindows()
with open(mark_file, "w") as f:
    for img_path, (id, x, y, w, h) in data_mark.items():
        f.write(f"{img_path},{id},{x},{y},{w},{h}\n")
