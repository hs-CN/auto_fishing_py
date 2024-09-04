import cv2
import os
import win32gui
from window_capture import WindowCapture

if not os.path.exists("./data/template.bmp"):
    print("模版文件'template.bmp'不存在")
    exit(0)

template = cv2.imread("./data/template.bmp", cv2.IMREAD_GRAYSCALE)
hwnd = win32gui.FindWindow(None, "魔兽世界")
if hwnd == 0:
    print("窗口未找到")
    exit(0)
else:
    print(f"窗口句柄:{hwnd}")
    window_capture = WindowCapture(hwnd)
    while True:
        img = window_capture.capture()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > 0.5:
            x, y = max_loc
            w, h = template.shape[::-1]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                img,
                f"{max_val:0.3f}",
                (x, y),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("q"):
            break
    cv2.destroyAllWindows()
