import time
from django.test import LiveServerTestCase

from selenium import webdriver


class VAccineFunctionalTest(LiveServerTestCase):
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
        super(VAccineFunctionalTest, self).setUp()

    def tearDown(self):
        self.browser.quit()
        super(VAccineFunctionalTest, self).tearDown()

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

    def test_add_vaccine(self):
        """Test add vaccine"""
        self.set_up_user()
        time.sleep(10)
        self.browser.find_element_by_class_name(
            'user-vaccine-add').click()
        expected_url = 'https://vacseen.herokuapp.com/vaccine/add/'
        self.assertEqual(self.browser.current_url, expected_url)
        time.sleep(10)
        self.browser.find_element_by_id(
            'vaccinename').send_keys('BCG')
        self.browser.find_element_by_id(
            'id_form-0-dose_count').send_keys(1)
        self.browser.find_element_by_class_name('save-btn').click()
        time.sleep(10)
        expected_url = 'https://vacseen.herokuapp.com/users/profile/'
        self.assertEqual(self.browser.current_url, expected_url)
        elements = self.browser.find_elements_by_id('vac-name-btn')
        elements_text = [ele.text for ele in elements]
        self.assertTrue('BCG' in elements_text)

    def test_delete_vaccine(self):
        """Test user signup vaccination"""
        self.set_up_user()
        time.sleep(5)
        self.browser.find_element_by_class_name(
            'user-vaccine-add').click()
        time.sleep(5)
        self.browser.find_element_by_id(
            'vaccinename').send_keys('Hepatitis A')
        self.browser.find_element_by_id(
            'id_form-0-dose_count').send_keys(1)
        self.browser.find_element_by_class_name('save-btn').click()
        elements = self.browser.find_elements_by_id('vac-name-btn')
        for element in elements:
            if element.text == 'Hepatitis A':
                element.click()
                time.sleep(5)
                self.browser.find_element_by_name('delvacc').click()
                break
        time.sleep(10)
        elements = self.browser.find_elements_by_id('vac-name-btn')
        elements_text = [ele.text for ele in elements]
        self.assertFalse('Hepatitis A' in elements_text)
