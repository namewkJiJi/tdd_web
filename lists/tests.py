from django.http import HttpRequest
from django.test import TestCase
from django.urls import resolve
from lists.views import home_page

class HomePageTest(TestCase):

    # 解析根目录，验证根路由解析的view是否是规定好的home_page函数
    # 如果根路由无法到home_page,可能是urls文件出现问题
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func,home_page)

    def test_home_page_return_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode("utf-8")
        self.assertTrue(html.startswith('<html>'))
        self.assertIn("<title>To-Do lists</title>",html)
        self.assertTrue(html.endswith("</html>"))
