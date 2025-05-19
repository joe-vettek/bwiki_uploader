import os
from selenium import webdriver
from selenium.webdriver.edge.options import Options


def create_driver(has=True):
    options = Options()
    # user_data_dir = os.path.abspath("cookie")
    user_data_dir = os.path.join(os.environ["USERPROFILE"],
                                 "AppData", "Local", "Microsoft", "Edge", "User Data")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    if has:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get("https://wiki.biligame.com/wiki/index.php?title=%E9%A6%96%E9%A1%B5")
    if not has:
        input("请登录完成后按回车继续...")
    return driver


def get_value(driver):
    keys = [c['value'] for c in driver.get_cookies() if c['domain'] == '.biligame.com' and c['name'] == "SESSDATA"]
    key = '' if len(keys) == 0 else keys[0]
    driver.close()
    return key


def main():
    cc = get_value(create_driver())
    if len(cc) == 0:
        cc = get_value(create_driver(False))
    return cc
