from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import datetime
import time
from bs4 import BeautifulSoup
from deta import Deta 
from dotenv import load_dotenv
load_dotenv()

##### Cron Job #####
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

deta = Deta(os.getenv('DETA_PROJECT_KEY'))
db = deta.Base("count-eunbin")

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

#################### PH ######################################################



ph_url = "https://www.etix.com/ticket/p/5171178/2022-park-eunbin-asia-fan-meeting-tour-in-manila-quezon-city-new-frontier-theater"

def app_ph(url,heroku=False):

    x = datetime.datetime.now()
    date_end = datetime.datetime(2022,10,23)
    if x > date_end:
        return

    ph_zone_list = ['PLATINUM-L','PLATINUM-C','PLATINUM-R','GOLD LFT','GOLD CTR','GOLD RGT','LOGE LFT','LOGE CTR','LOGE RGT','BAL-LEFT','BAL-CTR','BAL-RGT']
    ph_zone_data = ["PL","PC","PR","GL","GC","GR","SL","SC","SR","BL","BC","BR"]
    ph_total = [216,388,216,217,330,217,70,75,69,166,195,166]
    ph_count_reserved = []

    options = webdriver.chrome.options.Options()
    if not heroku:
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
    else:
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    
    for i in range(len(ph_zone_list)):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        driver.get(url)
        print(ph_zone_list[i])
        time.sleep(4)
        driver.execute_script("arguments[0].click();",driver.find_element(By.NAME,ph_zone_list[i]))
        time.sleep(4)
        # print(driver.current_url)
        html_doc = driver.page_source
        count = count_reserved(html_doc, "#seatingChartTbl .checkedTd")
        # check count == 0 bc that zone is not available
        if count == 0:
            ph_count_reserved.append(ph_total[i])
        else: 
            ph_count_reserved.append(count)
        driver.quit()
    print(ph_count_reserved)
    print(sum(ph_count_reserved))
    ph_count_available = subtract_arr(ph_total,ph_count_reserved)

    data = {"date": x.strftime("%Y-%m-%d %H:%M"), "country":"ph", "reserved": ph_count_reserved, "available": ph_count_available, "available_total": sum(ph_count_available), "reserved_total": sum(ph_count_reserved)}
    # print(data)
    db.put(data)


#################### TH ######################################################

th_url = "https://www.kokoconnection.com/EunBin_Note_Binkan_in_BKK/step.php"
def app_th(url,heroku=False):
    x = datetime.datetime.now()
    date_end = datetime.datetime(2022,11,5)
    if x > date_end:
        return

    th_total = [406,406,240,240,240,240,180,180]
    th_id_zone = ["seat_image_map_0", "seat_image_map_1","seat_image_map_2","seat_image_map_3","seat_image_map_4","seat_image_map_5","seat_image_map_6","seat_image_map_7"]

    th_count_reserved = []

    options = webdriver.chrome.options.Options()
    if not heroku:
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
    else:
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    
    for i in range(len(th_id_zone)):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
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



#################### SG ######################################################

sg_url = "https://allaccessasia.bigtix.io/booking/EUNBIN22"
def app_sg(url,heroku=False):
    x = datetime.datetime.now()
    date_end = datetime.datetime(2022,11,11)
    if x > date_end:
        return

    sg_id_zone = ["V1", "C1","C2"]
    sg_total = [466,384,65]
    sg_count_reserved = []
    sg_count_available = []

    options = webdriver.chrome.options.Options()
    if not heroku:
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
    else:
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    
    url = sg_url
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(5)
    element_submit = driver.find_element(By.ID,"bigtix-booking-next-page")
    element_submit.click()
    time.sleep(5)
    html_doc = driver.page_source
    driver.quit()

    for i in range(len(sg_id_zone)):
        print(sg_id_zone[i])
        time.sleep(3)
        # soup_one = BeautifulSoup(html_doc, 'html.parser')
        soup_two = BeautifulSoup(html_doc, 'html.parser')
        # all = soup_one.find_all(attrs={'data-seat-cat': sg_id_zone[i]})
        all_available = soup_two.find_all(attrs={'data-seat-cat': sg_id_zone[i], 'data-seat-status': "1"})
        # len_all = len(all)
        len_all_av = len(all_available)
        if len_all_av == 0:
            len_all_av == sg_total[i]
        len_all_re = sg_total[i]-len_all_av
        # sg_total.append(len_all)
        sg_count_available.append(len_all_av)
        sg_count_reserved.append(len_all_re)
    print(sg_count_reserved)
    print(sum(sg_count_reserved)) 

    data = {"date": x.strftime("%Y-%m-%d %H:%M"), "country":"sg", "reserved": sg_count_reserved, "available": sg_count_available, "available_total": sum(sg_count_available), "reserved_total": sum(sg_count_reserved)}
    # print(data)
    db.put(data)


####### Run Cron Job ########

@sched.scheduled_job('cron', day='1-31', hour=16)
def phsg_job():
    # app_ph(ph_url,True)
    app_sg(sg_url,True)

@sched.scheduled_job('cron', day='1-31', hour=17)
def th_job():
    app_th(th_url,True)
    
sched.start()