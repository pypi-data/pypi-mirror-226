"""
@Author: kang.yang
@Date: 2023/5/16 14:37
"""
import kuto

from page.web_page import IndexPage, LoginPage


class TestWebDemo(kuto.Case):

    def start(self):
        self.index_page = IndexPage(self.driver)
        self.login_page = LoginPage(self.driver)

    @kuto.title("登录")
    def test_login(self):
        self.open()
        self.index_page.loginBtn.click()
        self.login_page.pwdLoginTab.click()
        self.login_page.userInput.input('13652435335')
        self.login_page.pwdInput.input('wz123456@QZD')
        self.login_page.licenseBtn.click()
        self.login_page.loginBtn.click()
        self.login_page.firstCompanyIcon.click()
        self.login_page.assertContent("查专利")
        self.screenshot("首页")


if __name__ == '__main__':
    # 直接执行本文件，需要修改conf.yml中的platform
    kuto.main(
        platform="web",
        browser="chrome",
        host="https://www-test.qizhidao.com"
    )

