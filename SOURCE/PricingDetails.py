from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from ProjectManagementSoftware.Utilities import Reusable


class GetPirceDetails:

    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--blink-settings=imagesEnabled=false')
        # self.driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

    def getpriceDetails(self, url):
        self.getProductText(url)

    def getProductText(self, url):
        data = {}
        self.driver.get(url)
        WebDriverWait(self.driver, 5)
        try:
            element = self.driver.find_element_by_id('pricing')
            data['Pricing'] = element.text
            '''
            price_list = Reusable.splitString(element.text, '\n')
            data[price_list[0]] = price_list[1]
            data[price_list[2]] = price_list[3]
            data[price_list[4]] = price_list[5]
            '''
        except:
            data['Pricing'] = None




obj = GetPirceDetails()
obj.getpriceDetails('https://www.softwareadvice.com/project-management/openair-profile/')


