from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

class HomePageTest(TestCase):

    # 测试根路由是不是 home.html渲染网页
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response,"home.html")

    def test_can_save_a_POST_request(self):
        response = self.client.post('/',data={"item_text":"A new list item"})
        self.assertIn("A new list item",response.content.decode())
        self.assertTemplateUsed(response,"home.html")

    def test_home_page_return_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf-8")
        self.assertTrue(html.startswith('<html>'))
        self.assertIn("<title>To-Do lists</title>",html)
        self.assertTrue(html.endswith("</html>"))
