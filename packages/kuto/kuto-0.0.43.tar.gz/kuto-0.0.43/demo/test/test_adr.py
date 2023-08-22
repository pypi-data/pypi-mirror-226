import kuto

from page.adr_page import HomePage, \
    MyPage, SettingPage


class TestAdrDemo(kuto.Case):
    """安卓应用demo"""

    def start(self):
        self.home_page = HomePage(self.driver)
        self.my_page = MyPage(self.driver)
        self.set_page = SettingPage(self.driver)

    def test_1(self):
        self.home_page.myTab.click(timeout=10)
        self.my_page.settingBtn.click()
        self.set_page.assertActivity(
            '.me.MeSettingActivity')
        self.set_page.screenshot("设置页")


if __name__ == '__main__':
    kuto.main(
        platform='android',
        did='UJK0220521066836',
        pkg='com.qizhidao.clientapp'
    )


