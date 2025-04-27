import time
from selenium import webdriver
import unittest

from selenium.common import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser=webdriver.Chrome()
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID,"id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError,WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_start_a_list_retrieve_later(self):
        self.browser.get(self.live_server_url)

        # 网页的标题和头部都包含to-do这个词
        self.assertIn('To-Do',self.browser.title),"Browser title was: "+self.browser.title
        header_text = self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_text)

        # 应用有一个代办输入框
        input_box = self.browser.find_element(By.ID,"id_new_item")
        self.assertEqual(
            input_box.get_attribute("placeholder"),
            "Enter a to-do item"
        )

        input_box.send_keys("buy flowers")
        # 按下回车键后，页面会更新
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: buy flowers")
        # 应用又有一个代办输入框
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("give a gift to Lisi")
        input_box.send_keys(Keys.ENTER)


        # 页面会显示两个待办事项
        self.wait_for_row_in_list_table("1: buy flowers")
        self.wait_for_row_in_list_table("2: give a gift to Lisi")

        self.fail("Finish the test!")