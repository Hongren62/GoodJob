from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from datetime import datetime
import smtplib

path = "/Users/hongren/Desktop/chromedriver-mac-arm64/chromedriver"

service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

driver.get('https://www.104.com.tw/')

# 搜尋欄
search = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div/div/form/div/div/div[1]/div/input')
search.send_keys("軟體測試工程師")

# 選擇地區
region = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[1]/div/div/form/div/div/div[1]/div/div[1]/button')
region.click()

time.sleep(1)

# 選擇城市
city = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div/li[1]/a/span[1]/input')
city.click()

confirm = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[3]/button')
confirm.click()

search.send_keys(Keys.RETURN)

# 按照日期排序
select_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.ID, "js-sort"))
)
sort = Select(select_element)
sort.select_by_visible_text("日期排序")

for i in range(5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# 今日日期
now = datetime.now()
today_date = now.strftime('%m/%d')
today_date = today_date.lstrip('0').replace('/0', '/')

# 取得最新職缺數量
newJob = 0
job_titles = driver.find_elements(By.CLASS_NAME, "b-tit")
for job in job_titles:
    if job.text.startswith(today_date):
        newJob += 1

# 取得最新職缺連結
href_value = []
job_link = driver.find_elements(By.CSS_SELECTOR, "a.js-job-link")
for i, href in enumerate(job_link):
    if i >= newJob:
        break
    href_value.append(href.get_attribute('href'))

driver.quit()

formatted_href = '\n'.join(str(item) for item in href_value)

"""
將職缺連結寄送至信箱
"""

email = input("寄送人: ")
receiver_email = input("接收人: ")

subject = today_date + " 新增職缺"
message = "以下為 " + today_date + " 新增職缺：\n" + formatted_href

text = f"Subject: {subject}\n\n{message}"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

# google account app password
server.login(email, "")  

server.sendmail(email, receiver_email, text)
server.quit()