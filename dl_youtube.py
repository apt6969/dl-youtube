from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from PIL import Image

import concurrent.futures
import io
import time
import random
import os
import pickle
import sys
import csv
from datetime import datetime

def get_timestamp():
    timestamp = datetime.now()
    timestr = str(timestamp).replace(' ', '_')
    timestr = timestr.replace(':', '-')
    timestr = timestr[:-7]
    return timestr

def full_page_screenshot(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    parts = []

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(2)

        # Take screenshot
        part = Image.open(io.BytesIO(driver.get_screenshot_as_png()))
        parts.append(part)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Combine images into one
    full_img = Image.new('RGB', (parts[0].width, sum(p.height for p in parts)))
    offset = 0
    for part in parts:
        full_img.paste(part, (0, offset))
        offset += part.height

    return full_img

def dl_video(command):
    os.system(command)

def thread_dl_videos(commands, max_threads=20):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(dl_video, command) for command in commands]
        concurrent.futures.wait(futures)

def main():
    ser = Service('chromedriver')
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=ser, options=options)
    driver.set_window_size(1920, 1080*1)
    commands = []
    all_urls = []
    all_titles = []

    query_string = folder_string = ""
    for query in sys.argv[1:]:
        if query != "-NV":
            query_string += query + "+"
            folder_string += query + "_"
    query_string = query_string[:-1]
    folder_string = folder_string[:-1]
    
    os.system(f'mkdir screenshots > /dev/null 2>&1')
    os.system(f'mkdir videos > /dev/null 2>&1')
    os.system(f'mkdir csv > /dev/null 2>&1')
    os.system(f'mkdir videos/{folder_string} > /dev/null 2>&1')
    os.system(f'mkdir screenshots/{folder_string} > /dev/null 2>&1')
    os.system(f'mkdir csv/{folder_string} > /dev/null 2>&1')

    try:
        url = "https://www.youtube.com/results?search_query=" + query_string
        driver.get(url)
        time.sleep(random.uniform(2.75, 3.5))
        image = full_page_screenshot(driver)
        image.save(f"screenshots/{folder_string}/0_{get_timestamp()}.png")
        # driver.save_screenshot(f"screenshots/{folder_string}/0_{get_timestamp()}.png")
        all_urls.append(url)
        all_titles.append(query_string)
    except Exception as e:
        print(e)
        print(f"Failed to get original URL {url}")
        return

    for i in range(1, 20):
        try:
            link = driver.find_element(By.XPATH, f"//ytd-video-renderer[{i}]/div/div/div/div/h3/a/yt-formatted-string")
            text = link.text
            link.click()
            curr_url = driver.current_url
            print("Getting URL:", curr_url)
            time.sleep(random.uniform(2.75, 3.5))
            try:
                image = full_page_screenshot(driver)
                image.save(f"screenshots/{folder_string}/{i}_{get_timestamp()}.png")
                # driver.save_screenshot(f"screenshots/{folder_string}/{i}_{get_timestamp()}.png")
                print(f"Screenshot saved for {curr_url}")
                all_urls.append(curr_url)
                all_titles.append(text)
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            except Exception as e:
                print(e)
                print(f"Failed to save screenshot for {curr_url}")
            commands.append(f"yt-dlp --netrc-cmd '' -f 'bv*[height=480]+ba' --extractor-retries infinite -P videos/{folder_string}/ '{curr_url}'")
            # os.system(f"yt-dlp --netrc-cmd '' -f 'bv*[height=480]+ba' --extractor-retries infinite -P videos/{folder_string}/ '{curr_url}'")
            driver.back()
        except Exception as e:
            print(e)
            print(f"Failed to get URL for link number {i}")
            break
    
    for title in all_titles:
        title = title.replace(",", "_")
    
    with open(f"csv/{folder_string}/{get_timestamp()}.csv", "w") as f:
        writer = csv.writer(f)
        if len(all_urls) == len(all_titles):
            for idx, url in enumerate(all_urls):
                writer.writerow([idx, url, all_titles[idx]])
        else:
            for idx, url in enumerate(all_urls):
                writer.writerow([idx, url])

    if "-NV" not in sys.argv:
        # for command in commands:
        #     os.system(command)
        thread_dl_videos(commands, 20)
    print("Done! Quitting!")

if __name__ == "__main__":
    main()