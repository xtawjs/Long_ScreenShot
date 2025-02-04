import cv2
import numpy as np
import os
from numba import jit

min_input = input("预估相邻最小重叠度 min%, 输入min: ")
max_input = input("预估相邻最大重叠度 max%, 输入max: ")
# 尝试将输入转换为整数，如果失败或值为0，则将x设置为4
try:
    min_ = int(min_input)
    if min_ <= 0 or min_ >= 100:
        min_ = 50
except ValueError:  # 如果输入不是整数
    min_ = 50

try:
    max_ = int(max_input)
    if max_ <= min_ or max_ > 100:
        max_ = 99
except ValueError:  # 如果输入不是整数
    max_ = 99
print(f"设置的最小重叠度为：{min_}%")
print(f"设置的最大重叠度为：{max_}%")


@jit(nopython=True)
def calculate_similarity(row1, row2):
    """计算两行之间的相似度，这里简化为欧氏距离。"""
    return np.sqrt(np.sum((row1 - row2) ** 2))


def find_overlap_area(img1, img2):
    """查找两个图像之间的最佳重叠区域，假设以文字内容为主。"""
    max_overlap_height = int(img2.shape[0] * max_ * 0.01)
    min_overlap_height = int(img2.shape[0] * min_ * 0.01)

    best_overlap = 0
    lowest_similarity = float('inf')

    # 将图像转换为灰度以简化计算
    img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    for overlap_height in range(min_overlap_height, max_overlap_height):
        total_similarity = 0
        for row in range(overlap_height):
            img1_row = img1_gray[-overlap_height + row]
            img2_row = img2_gray[row]
            similarity = calculate_similarity(img1_row, img2_row)
            total_similarity += similarity

        avg_similarity = total_similarity / overlap_height

        if avg_similarity < lowest_similarity:
            lowest_similarity = avg_similarity
            best_overlap = overlap_height

    return best_overlap


def merge_images(img1, img2):
    """
    合并两个图像，假设第二个图像在底部，并且有重叠区域。
    """
    overlap_y_offset = find_overlap_area(img1, img2)
    overlap_height = img2.shape[0] - overlap_y_offset
    # 创建新图像
    new_height = img1.shape[0] + overlap_height
    new_image = np.zeros((new_height, img1.shape[1], 3), dtype=np.uint8)
    # 复制img1到新图像
    new_image[:img1.shape[0]] = img1
    # 合并img2的非重叠部分
    new_image[img1.shape[0]:] = img2[overlap_y_offset:]
    return new_image


def merge_all_images(folder_path):
    # 获取文件夹下的所有png文件
    files = [f for f in os.listdir(folder_path) if f.endswith('.png')]
    files.sort(key=lambda x: int(x.split('.')[0]))  # 按数字顺序排序

    if not files:
        print("No PNG files found in the folder.")
        return

    # 从1到n加载和合并图像
    current_image = cv2.imread(os.path.join(folder_path, files[0]))
    i = 0
    for file_name in files[1:]:
        i += 1
        next_image = cv2.imread(os.path.join(folder_path, file_name))
        current_image = merge_images(current_image, next_image)
        print(str(i) + '/' + str(len(files)))
    # 保存最终合并的图像
    cv2.imwrite('merged_image.png', current_image)
    print("Merged image saved.")


# 假设截图都放在当前目录下的shot文件夹内
folder_path = 'shot'
merge_all_images(folder_path)

os.startfile('.')
