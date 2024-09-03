import win32gui, win32ui
import ctypes
import cv2
import numpy as np


class WindowCapture:
    # 初始化
    def __init__(self, hwnd):
        # 窗口句柄
        self.hwnd = hwnd

        # 获取窗口的尺寸
        ctypes.windll.user32.SetProcessDPIAware()
        left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
        print(f"窗口矩形:left:{left} top:{top} right:{right} bottom:{bottom}")
        self.width = right - left
        self.height = bottom - top

        # 创建设备上下文（DC）
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()

        # 创建位图对象
        self.saveBitMap = win32ui.CreateBitmap()
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.width, self.height)
        self.saveDC.SelectObject(self.saveBitMap)

    def __del__(self):
        # 清理资源
        win32gui.DeleteObject(self.saveBitMap.GetHandle())
        self.saveDC.DeleteDC()
        self.mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwndDC)
        print("资源释放")

    def capture(self):
        # 截图 PrintWindow 函数第三个参数必须为2
        result = ctypes.windll.user32.PrintWindow(
            self.hwnd, self.saveDC.GetSafeHdc(), 2
        )
        if result:
            img = np.frombuffer(self.saveBitMap.GetBitmapBits(True), dtype=np.uint8)
            img.shape = (self.height, self.width, 4)
            return cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        else:
            return None


if __name__ == "__main__":
    hwnd = win32gui.FindWindow(None, "魔兽世界")
    if hwnd:
        print(f"窗口句柄:{hwnd}")
        window_capture = WindowCapture(hwnd)
        while True:
            img = window_capture.capture()
            cv2.imshow("window_capture", img)
            if cv2.waitKey(1) == ord("q"):
                break
    else:
        print("未找到窗口")
