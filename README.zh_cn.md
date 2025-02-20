# Long_ScreenShot

[Switch to English](./README.md)

Long_ScreenShot 是一个基于欧氏距离计算的长截图工具。它通过自动滚动屏幕并批量截取短图片，然后使用灰度图比较和欧氏距离最小化的方法，将短图片拼接成长截图。

## 功能特点

- **自动滚动截图**：自动滚动屏幕并批量截取短图片。
- **智能拼接**：通过比较前后两张短图片的灰度图，使用欧氏距离最小化算法确定拼接位置，实现无缝拼接。
- **参数可调**：支持自定义参数设置，适应不同的截图需求。
- **淡水印不敏感**：程序对淡水印不敏感，适合多种场景。
- **文字密集场景优化**：在文字密集场景下的拼接效果有一定优势。

## 使用方法

### 1. 运行 `shot.py`

1. 运行 `shot.py` 脚本。
2. 选取屏幕区域，程序将自动滚动并批量截取短图片，保存到临时文件夹中。

### 2. 运行 `splice.py`

1. 运行 `splice.py` 脚本。

2. 程序将上下滑动比较前后两张短图片的灰度图，使两个灰度图重叠部分的欧氏距离最小化，确定拼接位置并进行拼接。

   ![演示](./EXAMPLE.webp)

### 参数设置

- 在运行 `shot.py` 和 `splice.py` 时，可以设置参数。如果不填写参数，直接按下回车键，程序将按默认值运行。
- 如果发现截取或拼接效果不佳，可以调整参数以获得更好的效果。

## 注意事项

- **滚动截图区域**：请尽量不要在滚动截图区域中出现静止元素，以免影响拼接效果。
- **淡水印**：程序对淡水印不敏感，但仍建议在截图时避免大面积水印。
- 🤖**滚动截图过程中，鼠标指针请置于需滚动的窗口之上。**
- 🤖**程序检测到页面到底时自动停止滚动截图。按下esc键中止滚动截图。**

## 测试结果

经测试，Long_ScreenShot 在文字密集场景下的拼接效果有一定优势，能够较好地处理复杂的截图需求。

## 依赖项及许可证

本项目使用了以下第三方 Python 库：

| 依赖项         | 许可证                 |
| -------------- | ---------------------- |
| OpenCV (`cv2`) | Apache 2.0             |
| NumPy          | BSD 3-Clause           |
| Numba          | BSD 2-Clause           |
| Pillow (`PIL`) | PIL 许可证（MIT 兼容） |
| PyAutoGUI      | BSD 3-Clause           |
| Keyboard       | MIT                    |
| Tkinter        | Python 标准库          |
| Shutil         | Python 标准库          |

所有第三方库的许可证均与 MIT 兼容，如需详细了解，请参阅各库的官方文档或许可证文件。