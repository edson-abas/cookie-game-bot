from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time


def shop(items, cookie_num, my_driver):
    for item in items:
        if int(items[item]) <= cookie_num:
            clicker = my_driver.find_element(By.CSS_SELECTOR, f"#buy{item}")
            clicker.click()
            break
        else:
            continue


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

store = driver.find_element(By.CSS_SELECTOR, "#store")
store_list = [item.split(" - ") for index, item in enumerate(store.text.split("\n")) if index % 2 == 0]
store_dict = {key: value.replace(",", "") for (key, value) in store_list}
store_items = dict(reversed(list(store_dict.items())))

time_to_shop = time.time() + 5
timeout = time.time() + 60*5

cookie_button = driver.find_element(By.CSS_SELECTOR, "#cookie")

while time.time() < timeout:

    cookie_button.click()

    if time.time() > time_to_shop:
        money = driver.find_element(By.CSS_SELECTOR, "#money").text
        if "," in money:
            money = money.replace(",", "")
        cookies = int(money)
        shop(store_items, cookies, driver)
        time_to_shop = time.time() + 5


cookies_per_second = driver.find_element(By.XPATH, '//*[@id="cps"]').text
print(cookies_per_second)

driver.quit()
