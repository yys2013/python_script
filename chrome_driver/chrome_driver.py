#-*- coding:utf8 -*-


from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import os
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


#chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
chromedriver = "D:/bak/dev/ChromeDriver/75.0.3770.8/chromedriver_win32/chromedriver.exe"
#chromedriver_path = "C:/Program Files (x86)/Google/Chrome/Application"
chromedriver_path = "D:\\bak\\dev\\ChromeDriver\\75.0.3770.8\\chromedriver_win32"
os.environ["webdriver.chrome.driver"] = chromedriver

def chromeDriverNOBrowser():
    deriver_option = Options()
    #deriver_option.add_argument('--headless')
    deriver_option.add_argument('disable-infobars')
    deriver_option.add_argument('--no-sandbox')
    deriver_option.add_argument('--disable-dev-shm-usage')
    deriver_option.add_argument('--disable-gpu')
    #deriver_option.add_argument('blink-settings=imagesEnabled=false')

    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36"
    deriver_option.add_argument('user-agent=%s'%user_agent)
    #browser = webdriver.Firefox()
    browser = webdriver.Chrome(chrome_options=deriver_option)
    return browser

#chromedriver = "C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe"
#os.environ["webdriver.chrome.driver"] = chromedriver
#browser = webdriver.Chrome(chromedriver)

def preOrder(mac_url, username, password):
    browser = chromeDriverNOBrowser()
    browser.get(url)
    browser.maximize_window()

    WebDriverWait(browser,10)
    browser.find_element_by_name("add-to-cart").click()
    time.sleep(10)

    #https://www.apple.com/cn/shop/bag
    browser.find_element_by_id("shoppingCart.actions.checkout").click()
    time.sleep(10)

    WebDriverWait(browser,10)
    #https://secure2.store.apple.com/cn/shop/checkout?_s=Shipping-init
    if browser.find_element_by_id("loginHome.customerLogin.appleId"):
        browser.find_element_by_id("loginHome.customerLogin.appleId").send_keys(username)
    if browser.find_element_by_id("loginHome.customerLogin.password"):
        browser.find_element_by_id("loginHome.customerLogin.password").send_keys(password)
    if browser.find_element_by_id("signin-button-submit"):
        browser.find_element_by_id("signin-button-submit").click()
    time.sleep(10)

    #https://secure2.store.apple.com/cn/shop/checkout?_s=Shipping-init
    browser.find_element_by_id("checkout.shipping.fapiaoSelector.options.1").send_keys(Keys.SPACE)
    browser.find_element_by_id("checkout.shipping.fapiaoSelector.commerceFapiao.options.1").send_keys(Keys.SPACE)
    browser.find_element_by_id("checkout.shipping.fapiaoSelector.commerceFapiao.enterpriseFapiao.invoiceHeader").send_keys("何键东")
    browser.find_element_by_id("rs-checkout-continue-button").click()
    time.sleep(6)

    #https://secure2.store.apple.com/cn/shop/checkout?_s=Fulfillment-init
    browser.find_element_by_id("rs-checkout-continue-button").click()
    time.sleep(6)

    #https://secure2.store.apple.com/cn/shop/checkout?_s=Billing-init
    browser.find_element_by_id("checkout.billing.billingOptions.options.5-selector").click()
    time.sleep(6)
    browser.find_element_by_id("installments0000791680checkout.billing.billingOptions.selectedBillingOptions.installments.installmentOptions.options.4").send_keys(Keys.SPACE)
    browser.find_element_by_id("rs-checkout-continue-button").click()
    time.sleep(6)

    #https://secure2.store.apple.com/cn/shop/checkout?_s=Review
    browser.find_element_by_id("rs-checkout-continue-button").click()

    time.sleep(1000)
    #browser.find_element_by_id("kw").send_keys("python")
    #browser.find_element_by_id("su").click()
    #print(browser.page_source)
    browser.close()

if __name__ == '__main__':

    url = "https://www.apple.com/cn/shop/product/FR9Q2CH/A?fnode=9936a0c29742eae4c864495d97afc1dc1409e2b74dac4f31b90d2e87db976a82972ea40691b535ec32a73199d251712ca9e34dec5bdb84f0584c834694e588a4073900aa934e3e248c7fd2746c29992f"
    username = "XXX"
    password = "xxx"
    preOrder(url, username, password)
    time.sleep(10)
    # url = "http://www.baidu.com"
    # browser = chromeDriverNOBrowser()
    # browser.get(url)
    # browser.find_element_by_id("kw").send_keys("python")
    # browser.find_element_by_id("su").click()
    # print(browser.page_source)
    #order(url)
    #browser.close()