"""
@Author: kang.yang
@Date: 2023/8/1 18:21
"""
import cv2
import time
import os
import allure

from kuto.utils.log import logger
from kuto.utils.exceptions import ScreenFailException


def cut_by_position(image_path: str, position: str):
    """把图片按左上、左下、右上、右下进行分割"""
    # 读取图像
    image = cv2.imread(image_path)
    # 获取图像的宽度和高度
    height, width, _ = image.shape
    logger.debug(f'{height}, {width}')
    # 计算每个切割区域的宽度和高度
    sub_width = width // 2
    sub_height = height // 2
    # 切割图像成上下左右四个等份
    if position == "top_left":
        image_content = image[0:sub_height, 0:sub_width]
    elif position == "top_right":
        image_content = image[0:sub_height, sub_width:width]
    elif position == "bottom_left":
        image_content = image[sub_height:height, 0:sub_width]
    elif position == "bottom_right":
        image_content = image[sub_height:height, sub_width:width]
    else:
        raise KeyError("position传值错误")

    new_path = f"{image_path.split('.')[0]}_{position}.{image_path.split('.')[1]}"
    logger.debug(new_path)
    cv2.imwrite(new_path, image_content)
    return {
        "path": new_path,
        "height": height,
        "width": width
    }


def screenshot_util(driver, file_name=None, position: str = None):
    """
    截图并保存到预定路径
    @param driver
    @param file_name: foo.png or fool
    @param position: top_left\top_right\bottom_left\bottom_right
    @return:
    """
    logger.info("开始截图")
    start = time.time()
    if not file_name:
        raise ValueError("文件名不能为空")

    # 截图并保存到当前目录的image文件夹中
    relative_path = "image"
    try:
        # 把文件名处理成test.png的样式
        if "." in file_name:
            file_name = file_name.split(r".")[0]
        if os.path.exists(relative_path) is False:
            os.mkdir(relative_path)
        time_str = time.strftime(f"%Y%m%d%H%M%S")
        file_name = f"{time_str}_{file_name}.png"

        file_path = os.path.join(relative_path, file_name)
        # logger.info(f"save to: {os.path.join(relative_path, file_name)}")
        if getattr(driver, "info", None):
            driver.screenshot(file_path)
        else:
            driver.screenshot(path=file_path)
        # 对图片进行分割
        info = None
        if position is not None:
            info = cut_by_position(file_path, position)
            file_path = info.get("path")
        end = time.time()
        logger.info(f"截图完成，保存至: {file_path}，耗时: {end - start}s")
        # 上传allure报告
        allure.attach.file(
            file_path,
            attachment_type=allure.attachment_type.PNG,
            name=f"{file_path}",
        )
        if position is not None:
            return info
        else:
            return file_path
    except Exception as e:
        raise ScreenFailException(f"截图失败: \n{str(e)}")


