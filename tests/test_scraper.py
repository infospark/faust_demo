import unittest
from py import scraper
import undetected_chromedriver as uc


class TestWebScraping(unittest.TestCase):
    glassdoor_hastings_url = 'https://www.glassdoor.co.uk/Reviews/Hastings-Direct-Reviews-E230322.htm?filter.iso3Language=eng'
    glassdoor_home_url = 'https://www.glassdoor.co.uk/index.htm'
    bbc_home_url = 'https://www.bbc.com'

    @classmethod
    def setUpClass(cls):
        print("    setUpClass: " + cls.__name__ + " set up")
        cls.web_driver = uc.Chrome()

    @classmethod
    def tearDownClass(cls):
        print("    teardown: " + cls.__name__ + " set up")
        cls.web_driver.quit()

    def test_find_continue_with_google_button_on_glassdoor_homepage(self):
        self.web_driver.get(self.glassdoor_home_url)
        b = scraper.find_continue_with_google_button(self.web_driver)

        assert (b is not None, 'Could not find a Continue With Google Button')
        assert ("google" in b.get_attribute("class"))

    def test_login_with_google_on_glassdoor_homepage(self):
        scraper.login_with_google(web_driver=self.web_driver, url=self.glassdoor_home_url, username='jimplant@infospark.co.uk',
                                      password='fuZbif-rerkym-xeqve3')

        # How to assert I've logged in?
        # Look for something back on the home page

    def test_scrape_glassdoor_home_url(self):
        page_source = scraper.get_page_source(self.web_driver, self.glassdoor_home_url)
        assert ('Glassdoor' in page_source)

    def test_scrape_bbc_url(self):
        page_source = scraper.get_page_source(self.web_driver, self.bbc_home_url)
        assert ('BBC' in page_source)

    @unittest.skip("Currently fails because login is required")
    def test_scrape_paginated_url(self):
        for page_source in scraper.scrape_paginated_url(self.glassdoor_hastings_url):
            print(page_source[0:1000])
