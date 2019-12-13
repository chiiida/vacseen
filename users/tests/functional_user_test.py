import time
from django.test import LiveServerTestCase

from selenium import webdriver


class UserFunctionalTest(LiveServerTestCase):
    email = 'ttestuser189@gmail.com'
    password = '123456&&'
    firstname = 'testuser'
    lastname = 'lastname'
    phonenumber = '089998938'
    emer = '191'

    def setUp(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=options)
        super(UserFunctionalTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(UserFunctionalTest, self).tearDown()

    def set_up_user(self):
        """Setup user to login"""
        self.driver = webdriver.Chrome(executable_path="chromedriver")
        self.browser.get('https://vacseen.herokuapp.com/')
        self.browser.find_element_by_class_name('google-button').click()
        time.sleep(20)
        email = self.browser.find_element_by_xpath(
            '//*[@id="identifierId"]')
        email.send_keys(self.email)
        self.browser.find_element_by_id('identifierNext').click()
        time.sleep(20)
        password = self.browser.find_element_by_xpath(
            '//*[@name="password"]')
        password.send_keys(self.password)
        self.browser.find_element_by_id('passwordNext').click()
        time.sleep(10)

    def test_sign_up(self):
        """Test user signup"""
        self.set_up_user()
        self.browser.get(
            'https://vacseen.herokuapp.com/users/signup/')
        time.sleep(5)
        self.browser.find_element_by_id('firstname').send_keys(self.firstname)
        self.browser.find_element_by_id(
            'id_last_name').send_keys(self.lastname)
        self.browser.find_element_by_id(
            'id_contact').send_keys(self.phonenumber)
        self.browser.find_element_by_id(
            'id_emergency_contact').send_keys(self.emer)
        self.browser.find_element_by_class_name('next').click()
        time.sleep(5)
        expected_url = 'https://vacseen.herokuapp.com/users/signup/vaccination/'
        self.assertEqual(self.browser.current_url, expected_url)

    def test_vaccination_sign_up(self):
        """Test user signup vaccination"""
        self.set_up_user()
        self.browser.get(
            'https://vacseen.herokuapp.com/users/signup/vaccination/')
        time.sleep(5)
        self.browser.find_element_by_id(
            'vaccinename').send_keys('BCG')
        self.browser.find_element_by_id(
            'id_form-0-dose_count').send_keys(1)
        self.browser.find_element_by_id('terms-check-box').click()
        self.browser.find_element_by_class_name('save-btn').click()
        time.sleep(5)
        expected_url = 'https://vacseen.herokuapp.com/users/profile/'
        self.assertEqual(self.browser.current_url, expected_url)
