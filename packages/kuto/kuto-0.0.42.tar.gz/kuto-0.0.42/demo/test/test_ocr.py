"""
@Author: kang.yang
@Date: 2023/8/21 16:38
"""
import kuto
from page.ocr_page import OcrPage


class TestOcr(kuto.Case):

    def start(self):
        self.op = OcrPage(self.driver)

    def test_nanshan_wtt(self):
        self.op.searchBtn.click()
        self.op.searchInput.input("南山文体通")
        self.op.searchResult.click()
        self.op.schoolEntry.click()
        self.sleep(5)


if __name__ == '__main__':
    # 直接执行本文件，需要修改conf.yml中的platform
    kuto.main(
        platform='android',
        did='UJK0220521066836',
        pkg='com.tencent.mm')



