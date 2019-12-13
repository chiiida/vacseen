from django.test import LiveServerTestCase
from selenium import webdriver


class IndexFunctionalTest(LiveServerTestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=options)
        super(IndexFunctionalTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(IndexFunctionalTest, self).tearDown()

    def test_click_login(self):
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_class_name('google-button').click()
