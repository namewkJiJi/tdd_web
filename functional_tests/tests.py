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


    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("buy flowers")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: buy flowers")

        # 清单有一个唯一的url
        zhangsan_list_url = self.browser.current_url
        self.assertRegex(zhangsan_list_url,'/lists/.+')

        # 现在一个新用户访问网站
        self.browser.quit()
        self.browser = webdriver.Chrome()
        # 新用户访问首页，看不到之前用户的清单
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('buy flowers',page_text)
        self.assertNotIn('give a gift to Lisi',page_text)

        # 新用户输入一个新的待办事项，新建一个清单
        input_box = self.browser.find_element(By.ID, "id_new_item")
        input_box.send_keys("buy milk")
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: buy milk")

        # 王五获得了为一个url
        wangwu_list_url = self.browser.current_url
        self.assertRegex(wangwu_list_url,'/lists/.+')
        self.assertNotEqual(zhangsan_list_url,wangwu_list_url)

        # 这个页面还是没有张三的清单
        page_text = self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('buy flowers',page_text)
        self.assertIn('buy milk',page_text)

        self.fail("Finish the test!")

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            input_box.location['x']+input_box.size['width']/2,
            512,
            delta=10
        )
        input_box.send_keys("testing")
        input_box.send_keys(Keys.ENTER)
        input_box = self.browser.find_element(By.ID, "id_new_item")
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )
