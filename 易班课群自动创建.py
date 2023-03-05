import json
import time
from selenium.webdriver import Chrome
from selenium import webdriver

url = "https://www.yooc.me/group/create"

options = webdriver.ChromeOptions()
options.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"')
driver = Chrome(executable_path='chromedriver', options=options)


# options.add_argument("user-data-dir=selenium")


def getCookie(driver):
    # 设置cookie
    # web.delete_all_cookies()  # 删除所有的cookie
    # driver.add_cookie(
    #     {'domain': '.yooc.me', 'value': 'gCrVuIjnkv0KNIEfWXD6mV8znPrd5R5V', 'expiry': 'Thu, 29-Feb-2024 13:53:05 GMT',
    #      'Max-Age': '31449600', 'Path': '/', 'httpOnly': False,
    #      'HostOnly': False,
    #      'Secure': False})

    driver.get(url)  # selenium 模拟浏览器直接下载，该页面下载无需登录权限！
    # time.sleep(2)  # selenium 问题存在 反复请求之后需要登录，且下载加载缓慢
    time.sleep(20)
    dictCookies = driver.get_cookies()
    print(dictCookies)
    print(type(dictCookies))
    jsonCookies = json.dumps(dictCookies)  # dumps是将dict转化成str格式
    with open("selenium课群cookie保存.json", mode="w") as f:
        f.write(jsonCookies)

    driver.quit()


# getCookie()

def loadCookie(browser):
    with open('selenium课群cookie保存.json', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())  # loads是将str转化成dict格式

    # 往browser里添加cookies
    for cookie in listCookies:
        browser.get(url)  # todo 因为访问默认域名为 data，所以先访问，确定域名
        cookie_dict = {
            'domain': ".yooc.me",
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            "expires": '1680357633',
            'path': '/',
            'httpOnly': False,
            'HostOnly': False,
            'Secure': False
        }
        browser.add_cookie(cookie_dict)
    browser.refresh()


names = ["21数师" + str(i) + "班学习资料收集课群" for i in range(1, 4)] + ["21数应" + str(i) + "班学习资料收集课群" for i in range(1, 4)]
names += ["20数师" + str(i) + "班学习资料收集课群" for i in range(1, 4)] + ["20数应" + str(i) + "班学习资料收集课群" for i in range(1, 4)] + [
    "20大数据" + str(i) + "班学习资料收集课群" for i in range(1, 4)]
names += ["22数师" + str(i) + "班学习资料收集课群" for i in range(1, 4)] + ["22数应" + str(i) + "班学习资料收集课群" for i in range(1, 4)] + [
    "22大数据" + str(i) + "班学习资料收集课群" for i in range(1, 4)]


def create_class_group(driver):
    for name in names:
        class_name = driver.find_element_by_xpath('//*[@id="form"]/div[1]/input')
        class_name.send_keys(name)
        class_describe = driver.find_element_by_xpath('/html/body/section/form/div[4]/textarea')
        class_describe.send_keys(name)
        button = driver.find_element_by_xpath('//*[@id="form"]/input[14]')
        button.click()
        driver.get(url)


loadCookie(driver)
create_class_group(driver)
