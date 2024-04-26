import urllib
from urllib.parse import urljoin
from behave import given, when, then
from selenium.webdriver.common.by import By

@given("we want to add a product")
def user_on_product_newpage(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, '/product_new/')  # 确认这个URL是正确的
    context.browser.get(open_url)

@when("we fill in the form")
def user_fills_in_the_form(context):
    print(context.browser.page_source)  # 辅助调试
    name_textfield = context.browser.find_element(By.NAME, 'name')
    name_textfield.send_keys('thing one')
    price_textfield = context.browser.find_element(By.NAME, 'price')
    price_textfield.send_keys(3)
    context.browser.find_element(By.NAME, 'submit').click()

@then("it succeeds")
def product_added(context):
    assert 'thing one' in context.browser.page_source

@given(u'we have specific products to add')
def specific_products(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, '/product_new/')  # 确认这个URL是正确的
    for row in context.table:
        context.browser.get(open_url)
        name_textfield = context.browser.find_element(By.NAME, 'name')
        name_textfield.send_keys(row['name'])
        price_textfield = context.browser.find_element(By.NAME, 'price')
        price_textfield.send_keys(row['price'])
        context.browser.find_element(By.NAME, 'submit').click()
        assert row['name'] in context.browser.page_source

@when(u'we visit the listing page')
def step_impl(context):
    base_url = urllib.request.url2pathname(context.test_case.live_server_url)
    open_url = urljoin(base_url, '/')  # 根据路由设置，访问根目录
    context.browser.get(open_url)
    assert 'This is product' in context.browser.page_source, "Expected product listing not found."

@then(u'we will find \'another thing\'')
def step_impl(context):
    assert 'another thing' in context.browser.page_source, "Product 'another thing' not found on the page."