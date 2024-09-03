import win32gui, win32ui, win32con
import ctypes


def get_real_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def window_capture(hwnd):
    # 获取屏幕真实的尺寸
    screen_width, screen_height = get_real_resolution()
    print(f"屏幕尺寸:{screen_width}x{screen_height}")

    # 获取窗口的尺寸
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    print(f"窗口矩形:left:{left} top:{top} right:{right} bottom:{bottom}")
    width = right - left
    height = bottom - top

    # 创建设备上下文（DC）
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    # 创建位图对象
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    saveDC.SelectObject(saveBitMap)

    # 将屏幕内容复制到内存中
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, "desktop.bmp")
    print("截图成功")

    # 清理资源
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)


window_capture(win32gui.GetDesktopWindow())
