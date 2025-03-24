import time
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser=webdriver.Chrome()
    def tearDown(self):
        self.browser.quit()

    def test_start_a_list_retrieve_later(self):
        self.browser.get("http://localhost:8000")

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
        time.sleep(1)
        # 页面会显示1: buy flowers
        table = self.browser.find_element(By.ID,"id_list_table")
        rows = table.find_elements(By.TAG_NAME,"tr")
        self.assertIn('1: buy flowers',[row.text for row in rows])

        self.fail("Finish the test!")


if __name__ == '__main__':
    unittest.main()