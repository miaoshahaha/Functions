import pandas as pd 
import os
import requests

from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


# Scroll to the end to load all images.
def Scroll_To_End(driver):
    scroll_pause_time = 2.5

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    curr_num_button = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        sleep(scroll_pause_time)
        
        button = driver.find_elements(By.CLASS_NAME, 'mye4qd')
        
        # Button in the end of the driver window. 
        if len(button) > curr_num_button:       
            try:
                button[curr_num_button].click()
                curr_num_button += 1
                sleep(2)
            except:
                pass

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height


# Download all of the images from Google.
def Grab_Google_Image(driver, dir_name):
    
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    
    # Record number of file in directory
    n_files = len(os.listdir(dir_name))
    
    all_pics = driver.find_elements(By.CLASS_NAME, "Q4LuWd")
    pics = all_pics

    res = []
    checkset = set()

    for i in range(len(pics)):
        
        if i % 100 == 0:
            print(f"----------Current loading process : {i} / {len(pics)} ----------")
            
        try:  #For debug
            pics[i].click()
            sleep(0.5)
            
            pic_html = driver.find_elements(By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]')
            html = pic_html[0].get_attribute('src')
            
            if html not in checkset:
                res.append(html)
                checkset.add(html)
        except:
            print(f"[INFO] Pictures {i} not found")
            sleep(0.5)
            continue
        
    print("----------Finish Loading. ----------")            
    
    files_count = 1
    for i in range(len(res)):
        img_html = res[i]
        
        if i % 100 == 0:
            print(f"----------Current downloading process : {i} / {len(res)} ----------")
    
        try:
            response = requests.get(img_html)
            sleep(1)

            # Add n_files to save images from different query.
            with open(f"{dir_name}//image{files_count + n_files}.jpg", "wb") as f:
                f.write(response.content)

        except:
            print(f"[INFO] Couldn't find image number {i}. This message can be ignored.")
            continue

        files_count += 1
        
    print("----------Finish downloading. ----------")
        

# Search the images to be downloaded here. 
search_query = u'utaha kasumigaoka'
dir_name = u'霞之丘詩羽'

url = f'https://www.google.com/search?q={search_query}&tbm=isch'

driver = webdriver.Chrome()
driver.get(url)
sleep(5)

Scroll_To_End(driver)
Grab_Google_Image(driver, dir_name=dir_name)