"""
@Author: kang.yang
@Date: 2023/8/1 18:21
"""
import cv2
import time
import os
import allure

from kuto.utils.log import logger


def cut_half(image, position):
    if position == "up":
        return image[:image.shape[0] // 2, :]
    elif position == "down":
        return image[image.shape[0] // 2:, :]
    else:
        raise KeyError("position传值错误")


def cut_by_position(image_path: str, position: str):
    """把图片按左上、左下、右上、右下进行分割"""
    logger.info(position)
    # 读取图像
    logger.info("分割图片")
    start = time.time()
    image = cv2.imread(image_path)
    # 获取图像的宽度和高度
    height, width, _ = image.shape
    logger.debug(f'{height}, {width}')
    # 计算每个切割区域的宽度和高度
    sub_width = width // 2
    sub_height = height // 2
    # 切割图像成上下左右四个等份
    if "top_left" in position:
        image_content = image[0:sub_height, 0:sub_width]
        if position == "top_left_1":
            image_content = cut_half(image_content, "up")
        elif position == "top_left_2":
            image_content = cut_half(image_content, "down")
    elif "top_right" in position:
        image_content = image[0:sub_height, sub_width:width]
        if position == "top_right_1":
            image_content = cut_half(image_content, "up")
        elif position == "top_right_2":
            image_content = cut_half(image_content, "down")
    elif "bottom_left" in position:
        image_content = image[sub_height:height, 0:sub_width]
        if position == "bottom_left_1":
            image_content = cut_half(image_content, "up")
        elif position == "bottom_left_2":
            image_content = cut_half(image_content, "down")
    elif "bottom_right" in position:
        image_content = image[sub_height:height, sub_width:width]
        if position == "bottom_right_1":
            image_content = cut_half(image_content, "up")
        elif position == "bottom_right_2":
            image_content = cut_half(image_content, "down")
    else:
        raise KeyError(f"position传值错误 all: {position}")

    new_path = f"{image_path.split('.')[0]}_{position}.{image_path.split('.')[1]}"
    logger.debug(new_path)
    cv2.imwrite(new_path, image_content)
    cut_height, cut_width, _ = image_content.shape
    logger.debug(f'{cut_height, cut_width}')
    end = time.time()
    logger.info(f"分割成功， 耗时: {end - start}s")
    info = {
        "path": new_path,
        "height": height,
        "width": width,
        "cut_height": cut_height
    }
    logger.debug(info)
    return info


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
    # 把文件名处理成test.png的样式
    if "." in file_name:
        file_name = file_name.split(r".")[0]
    if os.path.exists(relative_path) is False:
        os.mkdir(relative_path)
    time_str = time.strftime(f"%Y%m%d%H%M%S")
    file_name = f"{time_str}_{file_name}.png"

    file_path = os.path.join(relative_path, file_name)
    start_screenshot = time.time()
    try:
        driver.screenshot(file_path)
    except:
        driver.screenshot(path=file_path)
    end_screenshot = time.time()
    logger.info(f"保存至: {file_path}")
    logger.info(f"截图耗时: {end_screenshot - start_screenshot}s")
    # 对图片进行分割
    info = None
    if position is not None:
        start_cut = time.time()
        info = cut_by_position(file_path, position)
        file_path = info.get("path")
        end_cut = time.time()
        logger.info(f"分割耗时: {end_cut - start_cut}s")
    # 上传allure报告
    start_upload = time.time()
    allure.attach.file(
        file_path,
        attachment_type=allure.attachment_type.PNG,
        name=f"{file_path}",
    )
    end_upload = time.time()
    logger.info(f"上传耗时: {end_upload - start_upload}s")
    end = time.time()
    logger.info(f"截图整体耗时: {end - start}s")
    if position is not None:
        return info
    else:
        return file_path


if __name__ == '__main__':
    cut_by_position('20230821101503_体育场馆.png', position="top_left_1")


