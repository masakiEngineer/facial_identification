from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime

driver = "chrome_driver_path"   # chrome_driver ver.114
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#Show browse or not
# options.add_argument('--headless')
browser = webdriver.Chrome(service=Service(driver), options=options)
browser.implicitly_wait(3)
url = "https://www.navitime.co.jp/transfer/"
browser.get(url)
time.sleep(2)


# 出発駅/到着駅の指定
START_STATION = "東京"
END_STATION = "有楽町"

# 会社から最寄り駅まで徒歩X分
COMPANY_TO_STATION = 10


# スクレイピング 文言指定
def sendString(element_string, sendKeyes_string):
    element = browser.find_element(By.CSS_SELECTOR, element_string)
    element.send_keys(sendKeyes_string)
    time.sleep(0.1)

# スクレイピング クリック
def click(element_string):
    element = browser.find_element(By.CSS_SELECTOR, element_string)
    element.click()
    time.sleep(0.5)

# スクレイピング テキスト取得
def getText(element_string):
    element = browser.find_element(By.CSS_SELECTOR, element_string)
    time.sleep(0.05)
    return element.text

# 「乗換案内」画面で乗車時刻・出発駅/到着駅の指定
def set_station_and_time():
    # 出発駅/到着駅指定
    sendString("#orv-station-name", START_STATION)
    sendString("#dnv-station-name", END_STATION)

    # 最寄り駅に到着する電車時刻
    current_minute = datetime.now().strftime('%M')
    current_hour = datetime.now().strftime('%H')
    train_minute = int(current_minute) + COMPANY_TO_STATION
    if (train_minute > 60):
        train_hour = int(current_hour) + 1
        train_minute = train_minute - 60
    else:
        train_hour = current_hour
    sendString("#hour", train_hour)
    sendString("#minute", train_minute)

    # 「検索」ボタン
    click("#search-area > form > div.submit-container > input[type=submit]")
    time.sleep(3)

# 電車発車時刻取得
def getTrainTimeList():
    print("------電車発車時刻------")
    for train_number in range(1, 4, 1):
        element_text = "#left_pane > ol.summary_list.print_target.recommend > li:nth-child(" + str(train_number) + ") > dl > dt"
        train_time = str(getText(element_text))
        train_time = train_time.split('⇒')[0].strip()
        print(train_time)

if __name__ == "__main__":
    set_station_and_time()
    getTrainTimeList()
