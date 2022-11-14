from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import os
import datetime
import time
from bs4 import BeautifulSoup
from deta import Deta 
from dotenv import load_dotenv
load_dotenv()

deta = Deta(os.getenv('DETA_PROJECT_KEY'))
db = deta.Base("count-eunbin")

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

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
# driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
# driver.get('http://google.com')
# print(driver.title)


#################### TH ######################################################

th_url = "https://www.kokoconnection.com/EunBin_Note_Binkan_in_BKK/step.php"
def app_th(url):
    x = datetime.datetime.now()
    # date_end = datetime.datetime(2022,11,5)
    # if x > date_end:
    #     return

    th_total = [406,406,240,240,240,240,180,180]
    th_id_zone = ["seat_image_map_0", "seat_image_map_1","seat_image_map_2","seat_image_map_3","seat_image_map_4","seat_image_map_5","seat_image_map_6","seat_image_map_7"]

    th_count_reserved = []
    
    for i in range(len(th_id_zone)):
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get(url)
        element_username = driver.find_element(By.NAME,"username")
        element_username.send_keys(os.getenv('USERNAME'))
        
        time.sleep(1)
        element_passwd = driver.find_element(By.NAME,"passwd")
        element_passwd.send_keys(os.getenv('PASSWORD'))
        time.sleep(1)
        element_submit = driver.find_element(By.NAME,"SUBMIT")
        element_submit.click()
        time.sleep(2)
        print(i)
        driver.execute_script("arguments[0].click();",driver.find_element(By.ID,th_id_zone[i]))
        time.sleep(3)
        # print(driver.current_url)
        html_doc = driver.page_source
        count = count_reserved(html_doc, "#format img")
        # check count == 0 bc that zone is not available
        if count == 0:
            th_count_reserved.append(th_total[i])
        else: 
            th_count_reserved.append(count)
        driver.quit()
    print(th_count_reserved)
    print(sum(th_count_reserved))
    th_count_available = subtract_arr(th_total,th_count_reserved)

    data = {"date": x.strftime("%Y-%m-%d %H:%M"), "country":"th", "reserved": th_count_reserved, "available": th_count_available, "available_total": sum(th_count_available), "reserved_total": sum(th_count_reserved)}
    # print(data)
    db.put(data)

app_th(th_url)
