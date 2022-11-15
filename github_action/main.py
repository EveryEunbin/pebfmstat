from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
#from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
#driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))


import os
import datetime
import time
from bs4 import BeautifulSoup
from deta import Deta 
from dotenv import load_dotenv
load_dotenv()

deta = Deta(os.getenv('DETA_PROJECT_KEY'))
db = deta.Base("count-eunbin")

# chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

def count_reserved(html_doc, css_selector):
    soup = BeautifulSoup(html_doc, 'html.parser')
    all = soup.select(css_selector)
    print(len(all))
    return len(all)

def subtract_arr(arrone,arrtwo):
    res = []
    for j in range(len(arrone)):
        res.append(arrone[j] - arrtwo[j])
    return res

## Simple example

# driver = webdriver.Chrome(options=chrome_options)
# driver.get('http://github.com')
# print(driver.title)
# driver.stop_client()
# driver.close()
# driver.quit()


#################### MY ######################################################

my_url = "https://www.excitix.com.my/user/login" 
def app_my(url):
    x = datetime.datetime.now()
    date_end = datetime.datetime(2022,12,24)
    if x > date_end:
        return

    my_total = [500,500,300,300,380,380]
    my_zone = ["VIPL", "VIPR", "CAT1L", "CAT1R", "CAT2L", "CAT2L"]
    my_zone_url = [179,180,181,182,183,184]
    my_count_reserved = []
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    element_username = driver.find_element(By.NAME,"username")
    element_username.send_keys(os.getenv('USERNAME'))
    time.sleep(1)
    element_passwd = driver.find_element(By.NAME,"password")
    element_passwd.send_keys(os.getenv('PASSWORD'))
    time.sleep(1)
    element_submit = driver.find_element(By.XPATH,"//button[@type='submit']")
    element_submit.click()
    time.sleep(2)

    for i in range(len(my_zone)):
        print(my_zone[i])
        script = "window.location.replace('https://www.excitix.com.my/checkout/{}')".format(my_zone_url[i])
        driver.execute_script(script)
        time.sleep(5)
        html_doc = driver.page_source
        count = count_reserved(html_doc, ".occupied")
        my_count_reserved.append(count)
    driver.quit()
    print(my_count_reserved)
    print(sum(my_count_reserved))
    my_count_available = subtract_arr(my_total,my_count_reserved)
    data = {"date": x.strftime("%Y-%m-%d %H:%M"), "country":"my", "reserved": my_count_reserved, "available": my_count_available, "available_total": sum(my_count_available), "reserved_total": sum(my_count_reserved)}
    print(data)
    db.put(data)

app_my(my_url)
