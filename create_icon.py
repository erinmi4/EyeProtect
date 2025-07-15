"""
图标生成器
为系统托盘创建护眼提醒器图标
"""
from PIL import Image, ImageDraw
import os


def create_eye_icon(size=64, filename="icon.png"):
    """
    创建眼睛图标
    
    Args:
        size: 图标大小
        filename: 保存文件名
    """
    # 创建图像
    image = Image.new('RGBA', (size, size), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    
    # 计算相对尺寸
    padding = size // 8
    
    # 绘制眼睛外轮廓（椭圆形）
    eye_left = padding
    eye_top = size // 3
    eye_right = size - padding
    eye_bottom = size * 2 // 3
    
    # 眼睛背景（白色）
    draw.ellipse([eye_left, eye_top, eye_right, eye_bottom], 
                fill=(255, 255, 255, 255), outline=(100, 149, 237, 255), width=2)
    
    # 虹膜（浅蓝色）
    iris_size = (eye_right - eye_left) // 2
    iris_left = (size - iris_size) // 2
    iris_top = eye_top + (eye_bottom - eye_top - iris_size) // 2
    iris_right = iris_left + iris_size
    iris_bottom = iris_top + iris_size
    
    draw.ellipse([iris_left, iris_top, iris_right, iris_bottom], 
                fill=(135, 206, 250, 255), outline=(70, 130, 180, 255), width=1)
    
    # 瞳孔（黑色）
    pupil_size = iris_size // 2
    pupil_left = (size - pupil_size) // 2
    pupil_top = iris_top + (iris_size - pupil_size) // 2
    pupil_right = pupil_left + pupil_size
    pupil_bottom = pupil_top + pupil_size
    
    draw.ellipse([pupil_left, pupil_top, pupil_right, pupil_bottom], 
                fill=(0, 0, 0, 255))
    
    # 高光（白色小点）
    highlight_size = pupil_size // 3
    highlight_left = pupil_left + pupil_size // 4
    highlight_top = pupil_top + pupil_size // 4
    highlight_right = highlight_left + highlight_size
    highlight_bottom = highlight_top + highlight_size
    
    draw.ellipse([highlight_left, highlight_top, highlight_right, highlight_bottom], 
                fill=(255, 255, 255, 255))
    
    # 添加眼睫毛（上方几条小线）
    lash_color = (64, 64, 64, 255)
    lash_width = 2
    
    # 左侧睫毛
    draw.line([eye_left + size//8, eye_top - 3, eye_left + size//6, eye_top - 8], 
             fill=lash_color, width=lash_width)
    
    # 中间睫毛
    draw.line([size//2 - 2, eye_top - 5, size//2 + 2, eye_top - 10], 
             fill=lash_color, width=lash_width)
    
    # 右侧睫毛
    draw.line([eye_right - size//6, eye_top - 8, eye_right - size//8, eye_top - 3], 
             fill=lash_color, width=lash_width)
    
    return image


def create_all_icons():
    """创建不同尺寸的图标"""
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建不同尺寸的图标
    sizes = [16, 32, 64, 128]
    
    for size in sizes:
        icon = create_eye_icon(size)
        filename = f"icon_{size}x{size}.png"
        filepath = os.path.join(current_dir, filename)
        icon.save(filepath, "PNG")
        print(f"已创建图标: {filename}")
    
    # 创建默认图标
    default_icon = create_eye_icon(64)
    default_filepath = os.path.join(current_dir, "icon.png")
    default_icon.save(default_filepath, "PNG")
    print(f"已创建默认图标: icon.png")
    
    return default_filepath


if __name__ == "__main__":
    create_all_icons()
