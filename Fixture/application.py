from selenium import webdriver
from Fixture.session import SessionHelper
from Fixture.group import GroupHelper
from Fixture.contacts import AddressHelper


class Application:


    def __init__(self, browser, base_Url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.wd.implicitly_wait(10)
        self.session = SessionHelper(self)
        self.group = GroupHelper(self)
        self.Contacts = AddressHelper(self)
        self.base_Url = base_Url

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False



    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_Url)


    def destroy(self):
        self.wd.quit()