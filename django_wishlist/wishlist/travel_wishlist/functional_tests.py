import selenium
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from django.test import LiveServerTestCase

class TitleTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_title_shown_on_home_page(self):
        self.selenium.get(self.live_server_url)
        assert 'Travel Wishlist' in self.selenium.title


class AddEditPlacesTests(LiveServerTestCase):

    fixtures = ['test_places']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)


    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


    def test_add_new_place(self):

        # Load home page
        self.selenium.get(self.live_server_url)
        # Find input text box. id was genereated by django forms
        input_name = self.selenium.find_element_by_id('id_name')
        # Enter place name
        input_name.send_keys('Denver')
        # Find the add button
        add_button = self.selenium.find_element_by_id('add-new-place')
        # And click button
        add_button.click()

        # Got to make this test code wait for the server to process the request and for page to reload
        # wait for new element to appear on page
        wait_for_denver = self.selenium.find_element_by_id('place-name-5')

        # Assert places from test_places are on page
        assert 'Tokyo' in self.selenium.page_source
        assert 'New York' in self.selenium.page_source

        # new place is added
        assert 'Denver' in self.selenium.page_source