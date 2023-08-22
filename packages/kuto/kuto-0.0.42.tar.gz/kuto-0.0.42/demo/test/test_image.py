"""
@Author: kang.yang
@Date: 2023/8/21 16:38
"""
import kuto
from page.image_page import ImagePage


class TestOcr(kuto.Case):

    def start(self):
        self.ip = ImagePage(self.driver)

    def test_nanshan_wtt(self):
        self.ip.searchEntry.click()
        self.ip.searchInput.input("南山文体通")
        self.ip.searchResult.click()
        self.ip.schoolEntry.click()
        self.sleep(5)


if __name__ == '__main__':
    # 直接执行本文件，需要修改conf.yml中的platform
    kuto.main(
        platform='android',
        did='UJK0220521066836',
        pkg='com.tencent.mm')



