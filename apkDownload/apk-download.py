import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
noElement = "Failed to locate element."
def debug_print(content, type="url"):
    if type == "url":
        print("Currently at: ", content)
    elif type == "title":
        print("Site's title: ", content)

chromeOptions = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ChromeService(
    ChromeDriverManager().install()), options=chromeOptions)
driver.implicitly_wait(5)
cleanList = []

with open("download2.csv",'r') as read_obj:
    csv_reader = csv.reader(read_obj)
    for row in csv_reader:
        apk_name = str(row[0])
        try:
            driver.get("https://apkpure.com/search?q="+apk_name)
            driver.implicitly_wait(5)
            debug_print(driver.title, "title")
            debug_print(driver.current_url)
            download_element = driver.find_element(By.CLASS_NAME, "first-info")
            download_a_tag = download_element.find_element(By.TAG_NAME, "a")
            driver.get(download_a_tag.get_attribute("href"))
            driver.implicitly_wait(5)
            debug_print(driver.title, "title")
            go_to_download = driver.find_element(By.CLASS_NAME, "go-to-download")
            driver.get(go_to_download.get_attribute("href"))
            debug_print(driver.current_url)
            download_box = driver.find_element(By.CLASS_NAME, "download-box")
            download_link = download_box.find_element(By.TAG_NAME, "a")
            if apk_name in download_link.get_attribute("href"):
                if apk_name != 'y':
                    driver.get(download_link.get_attribute("href"))
                    print("PASS")
                    print("Downloading....")
                    cleanList.append([row[0]])
                else:
                    cleanList.append(['x'])
            else:
                print("FAILED")
                print("APK not found.")
                cleanList.append(['x'])
            time.sleep(5)
        except NoSuchElementException as e:
            print(noElement)
            print("FAILED")
            print("APK was not found, APK is outdated or APK name is incorrect.")
        except Exception as e:
            print("FAILED")
            print("Another exception occurred: \n", e)

driver.quit()
print("SAVING RESULTS...")
with open('downloaded.csv','w+',encoding='UTF8') as cleanFile:
    writer = csv.writer(cleanFile)
    for row in cleanList:
        writer.writerow(row)
print("DONE.")