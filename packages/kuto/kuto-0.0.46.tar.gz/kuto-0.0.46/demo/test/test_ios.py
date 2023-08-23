import kuto

from page.ios_page import IndexPage, MyPage


class TestIosDemo(kuto.Case):
    """IOS应用demo"""

    def start(self):
        self.index_page = IndexPage(self.driver)
        self.my_page = MyPage(self.driver)

    def test_go_setting(self):
        self.index_page.myTab.click()
        self.my_page.settingBtn.click()
        self.my_page.assertContent("设置")


if __name__ == '__main__':
    kuto.main(
        platform="ios",
        did='00008101-000E646A3C29003A',
        pkg='com.qizhidao.company'
    )


