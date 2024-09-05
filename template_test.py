import sys
import cv2
import os

if not os.path.exists("./template.bmp"):
    print("模版文件'template.bmp'不存在")
    exit(0)

template = cv2.imread("./template.bmp", cv2.IMREAD_GRAYSCALE)

if len(sys.argv) != 2:
    print("参数错误")
    exit(0)

data_folder = sys.argv[1]
img_files = [
    (os.path.join(data_folder, name), name, int(name[:-4]))
    for name in os.listdir(data_folder)
    if name.endswith(".jpg")
]
img_files.sort(key=lambda x: x[2])

for img_file, img_name, _ in img_files:
    img = cv2.imread(img_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val > 0.6:
        x, y = max_loc
        w, h = template.shape[::-1]
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            img, f"{max_val:0.3f}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
    cv2.putText(
        img,
        img_name,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )
    cv2.imshow("img", img)
    if cv2.waitKey(1) == ord("q"):
        break
