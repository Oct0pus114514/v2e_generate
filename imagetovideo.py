import cv2
import numpy as np
from PIL import Image
import os
from natsort import natsorted
import argparse

def images_to_video(input_folder, output_video, fps=24, size=None):
    """
    将文件夹中的图片转换为视频
    
    参数:
    input_folder (str): 输入图片文件夹路径
    output_video (str): 输出视频文件路径（例如：output.mp4）
    fps (int): 视频帧率（默认24）
    size (tuple): 视频尺寸（宽度, 高度），默认使用第一张图片尺寸
    """
    
    # 获取所有图片文件并按自然顺序排序
    valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
    images = [f for f in os.listdir(input_folder) 
             if os.path.splitext(f)[1].lower() in valid_extensions]
    
    if not images:
        print("错误：文件夹中没有找到支持的图片格式")
        return
    
    images = natsorted(images)  # 自然排序（正确处理数字顺序）
    
    # 确定视频尺寸
    first_img_path = os.path.join(input_folder, images[0])
    with Image.open(first_img_path) as first_img:
        if size is None:
            size = first_img.size  # 使用第一张图片尺寸
        else:
            first_img.verify()  # 检查文件完整性

    # 初始化视频写入器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 编解码器
    video_writer = cv2.VideoWriter(output_video, fourcc, fps, size)
    
    if not video_writer.isOpened():
        print(f"错误：无法创建视频文件 {output_video}")
        return

    # 处理每张图片
    for image_name in images:
        img_path = os.path.join(input_folder, image_name)
        
        try:
            # 使用Pillow读取图片并转换为RGB模式
            with Image.open(img_path).convert('RGB') as img:
                # 调整尺寸并转换为numpy数组
                img = img.resize(size)
                frame = np.array(img)
                # 转换颜色空间（Pillow使用RGB，OpenCV需要BGR）
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"警告：跳过无法处理的文件 {image_name} - {str(e)}")
            continue
        
        video_writer.write(frame)

    # 释放资源
    video_writer.release()
    print(f"视频已成功保存至：{output_video}")

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--input_folder',type=str,required=True,help='输入图片文件夹路径')
    parser.add_argument('-o','--output_video',type=str,required=True,help='输出视频文件路径')
    parser.add_argument('-f','--fps',type=int,help='视频帧率',default=240)
    input_folder = parser.parse_args().input_folder
    output_video = parser.parse_args().output_video
    fps=parser.parse_args().fps
    
    # 调用转换函数
    images_to_video(
        input_folder,
        output_video,
        fps=fps,            # 可调整帧率
    )