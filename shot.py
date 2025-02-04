import tkinter as tk
from PIL import ImageGrab
import pyautogui
import time
import os
import cv2
import numpy as np
import keyboard
import shutil

p_input = input("每次滚动 1/p 选定窗口高度, 输入p: ")
t_input = input("滚动间隔 t秒, 输入t: ")
# 尝试将输入转换为整数，如果失败或值为0，则将x设置为4
try:
    p = int(p_input)
    if p <= 0:
        p = 4
except ValueError:
    p = 4
print(f"设置的滚动比例为：1/{p}")
try:
    t = float(t_input)
    if t <= 0:
        t = 1.0
except ValueError:
    t = 1.0
print(f"设置的滚动间隔为：{t}秒")
time.sleep(1)
# 设置截图保存的文件夹
screenshot_folder = "shot"
if not os.path.exists(screenshot_folder):
    os.makedirs(screenshot_folder)
else:
    shutil.rmtree(screenshot_folder)
    os.makedirs(screenshot_folder)
# 初始化选择器
root = tk.Tk()
root.attributes("-fullscreen", True)
root.wait_visibility(root)
root.attributes("-alpha", 0.3)  # 设置透明度
canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)


def on_click(event):
    canvas.delete("rect")
    global start_x, start_y
    start_y = event.y
    start_x = event.x


def on_drag(event):
    global rect
    end_x, end_y = event.x, event.y
    canvas.delete("rect")
    rect = canvas.create_rectangle(start_x, start_y, end_x, end_y, outline='red', tag="rect")


def on_release(event):
    global selection_made
    selection_made = True
    root.quit()






selection_made = False
canvas.bind("<ButtonPress-1>", on_click)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)

# 显示选择器窗口并等待用户选择区域
root.mainloop()

# 获取用户选择的区域坐标
rect_coords = canvas.coords("rect")
root.destroy()
# 用户未作出选择，退出程序
if not selection_made or len(rect_coords) != 4:
    exit()
# 确定滚动距离为区域高度的一半

scroll_distance = int((rect_coords[3] - rect_coords[1]) / p)

# 滚动并截图
scroll_pause_time = t  # 每次滚动后的暂停时间
last_image = None


def on_esc_press(e):
    global keep_running
    keep_running = False


# 监听ESC键
keyboard.on_press_key("esc", on_esc_press)

keep_running = True
i = 0
while keep_running:
    i += 1
    # 截图保存
    image_path = os.path.join(screenshot_folder, f"{i:03}.png")
    ImageGrab.grab(bbox=rect_coords).save(image_path)

    # 加载图片并转换为灰度图
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    if last_image is not None:
        # 计算两个图像之间的相似性
        difference = cv2.absdiff(last_image, gray_image)
        if np.sum(difference) < 1:  # 如果变化非常小，认为到达底部
            print("到达底部，停止滚动")
            os.remove(image_path)
            break

    last_image = gray_image

    # 模拟滚动
    scroll_amount = -int(scroll_distance)  # pyautogui的scroll函数期望一个整数值
    pyautogui.scroll(scroll_amount)
    time.sleep(scroll_pause_time)  # 等待页面加载

    # 如果按下ESC键，退出
    if keyboard.is_pressed("esc"):
        print("检测到ESC键，退出程序")

        break

print("完成截图")
keyboard.unhook_all()  # 移除所有键盘钩子

'''
# 读取并拼接截图
def stitch_images(folder_path, scroll_amount):
    # 读取所有截图文件名，按文件名排序以确保正确的顺序
    images = sorted([img for img in os.listdir(folder_path) if img.endswith(".png")],
                    key=lambda x: int(x.split('.')[0]))
    # 初始化一个空列表来存储裁剪过的图片
    cropped_images = []
    for i, image_name in enumerate(images):
        # 读取图片
        img_path = os.path.join(folder_path, image_name)
        img = cv2.imread(img_path)
        # 除了最后一张图片外，所有图片都按照滚动量裁剪掉底部
        if i != len(images) - 1:
            cropped_img = img[:-scroll_amount, :]
        else:
            cropped_img = img
        cropped_images.append(cropped_img)

    # 使用np.vstack垂直堆叠图片
    final_image = np.vstack(cropped_images)
    # 保存最终的图片
    final_image_path = os.path.join(folder_path, "final_stitched_image.png")
    cv2.imwrite(final_image_path, final_image)
    print(f"图片拼接完成，保存为 {final_image_path}")


# 调用函数进行图片拼接，注意传递滚动距离的绝对值，因为之前设置scroll_amount为负值
stitch_images(screenshot_folder, abs(scroll_amount))
'''
