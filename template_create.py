import sys
import cv2

if len(sys.argv) != 2:
    print("参数错误")
    exit(0)

img_path = sys.argv[1]
img = cv2.imread(img_path)
cv2.imshow("img", img)
x, y, w, h = cv2.selectROI("img", img, showCrosshair=False)
template = img[y : y + h, x : x + w]
cv2.imshow("img", template)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("./template.bmp", template)
