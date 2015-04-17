from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class SeleniumEasy(object):
    def __init__(self, url, user_agent=None):
        self.url = url
        self.driver = webdriver.Firefox(firefox_profile=self.firefox_useragent(user_agent))
        self.driver.get(url)
        self.timeout = 3
        self.main_window_handler = self.driver.current_window_handle

    def close(self):
        self.driver.quit()

    def click(self, by_id, element):
        if not By.is_valid(by_id):
            raise KeyError, 'Invalid input({0}). Use <from selenium.webdriver.common.by import By>.'.format(by_id)
        try:
            WebDriverWait(self.driver, self.timeout).until(lambda x: x.find_element(by_id, element))
        except TimeoutException:
            print "no element {0}".format(element)
        elm = self.driver.find_element(by_id, element)
        elm.click()

    def input(self, by_id, element, value):
        if not By.is_valid(by_id):
            raise KeyError, 'Invalid input({0}). Use <from selenium.webdriver.common.by import By>.'.format(by_id)
        try:
            WebDriverWait(self.driver, self.timeout).until(lambda x: x.find_element(by_id, element))
        except TimeoutException:
            print "no element {0}".format(element)
        elm = self.driver.find_element(by_id, element)
        elm.clear()
        elm.send_keys(ur'{0}'.format(value))

    def alert_cofirm(self):
        return self.__alert__(True)

    def alert_cancel(self):
        return self.__alert__(False)

    def __alert__(self, bool):
        try:
            WebDriverWait(self.driver, self.timeout).until(expected_conditions.alert_is_present(), 'Timed out waiting for popup alert')
            alert = self.driver.switch_to_alert()
            if bool:
                alert.accept()
                print "alert accepted"
            else:
                alert.dismiss()
                print "alert canceld"
        except TimeoutException:
            print "no alert"

    def popup_window(self, handle=None):
        if handle is None:
            print 'change window {0} > {1}'.format(self.main_window_handler, self.driver.window_handles[-1])
            self.driver.switch_to_window(self.driver.window_handles[-1])
        else:
            print 'change window {0} > {1}'.format(self.main_window_handler, handle)
            self.driver.switch_to_window(handle)

    def popup_window_close(self, handle=None):
        if handle is None:
            for handle in self.driver.window_handles:
                if handle == self.main_window_handler:
                    continue
                self.driver.switch_to_window(handle)
                self.driver.close()
        else:
            self.driver.switch_to_window(handle)
            self.driver.close()

    def main_window(self):
        self.driver.close()
        self.driver.switch_to_window(self.main_window_handler)

    def firefox_useragent(self, user_agent):
        from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
        profile = FirefoxProfile()
        if user_agent is not None:
            if user_agent == 'mobile':
                user_agent = 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
            profile.set_preference('general.useragent.override', user_agent)
        return profile

