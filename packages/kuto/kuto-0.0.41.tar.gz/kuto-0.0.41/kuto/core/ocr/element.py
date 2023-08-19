import time

from kuto.utils.log import logger
from kuto.core.ocr.ocr_discern import OCRDiscern
from kuto.utils.exceptions import ElementNameEmptyException


class OCRElem(object):
    """ocr识别定位"""

    def __init__(self, driver=None, text: str = None, position: str = None):
        """
        @param driver:
        @param text:
        @param position: top_left、top_right、bottom_left、bottom_right
        """
        self.driver = driver
        self.text = text
        self._position = position

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self.driver = instance.driver
        return self

    def exists(self, retry=3, timeout=1):
        logger.info(f'ocr识别文本: {self.text} 是否存在')
        time.sleep(3)
        for i in range(retry):
            logger.info(f'第{i+1}次查找:')
            image_path = self.driver.screenshot(self.text, position=self._position)
            res = OCRDiscern(image_path).get_coordinate(self.text)
            if isinstance(res, tuple):
                self.driver.screenshot(f'ocr识别定位-{self.text}')
                return True
            time.sleep(timeout)
        else:
            self.driver.screenshot(f'ocr识别定位失败-{self.text}')
            return False

    def click(self, retry=3, timeout=1):
        logger.info(f'ocr点击文本: {self.text}')
        time.sleep(3)
        for i in range(retry):
            logger.info(f'第{i+1}次查找:')
            info = self.driver.screenshot(self.text, position=self._position)
            image_path = info.get("path")
            width = info.get("width")
            height = info.get("height")
            res = OCRDiscern(image_path).get_coordinate(self.text)
            if isinstance(res, tuple):
                x, y = res
                if self._position == 'top_right':
                    x = width/2 + x
                    y = y
                elif self._position == 'top_left':
                    x = x
                    y = y
                elif self._position == 'bottom_left':
                    x = x
                    y = height/2 + y
                elif self._position == 'bottom_right':
                    x = width/2 + x
                    y = height/2 + y
                logger.info(f'识别坐标为: ({x}, {y})')
                self.driver.click(x, y)
                return
            time.sleep(timeout)
        else:
            self.driver.screenshot(f'ocr识别定位失败-{self.text}')
            raise Exception('通过OCR未识别指定文字或置信度过低，无法进行点击操作！')


if __name__ == '__main__':
    from kuto.core.android.driver import AndroidDriver

    driver = AndroidDriver(device_id='UJK0220521066836', pkg_name='com.qizhidao.clientapp')
    # driver.start_app()
    elem = OCRElem(driver, text='体育场馆', position="top_left")
    # all - 850, 938
    # top_right - 307, 938
    # all -
    elem.click()

