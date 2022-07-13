from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import bs4
import requests
import os
import time

#ser = Service(r"C:\Users\Samuel Mensah\RipeDetect\chromedriver.exe")
driver = webdriver.Chrome(r"C:\Users\Samuel Mensah\RipeDetect\chromedriver.exe")
classes = ["riped tomato", "unriped tomato"]

ripe = r"C:\Users\Samuel Mensah\RipeDetect\img_dataset\valid\riped"
unripe = r"C:\Users\Samuel Mensah\RipeDetect\img_dataset\valid\Unriped"

folders = [ripe, unripe]
queries = ["https://www.google.com/search?q=riped+tomato&tbm=isch&ved=2ahUKEwja08G7iez4AhUHWxoKHabkDGAQ2-cCegQIABAA&oq=riped+tomato&gs_lcp=CgNpbWcQARgAMgQIIxAnMgUIABCABDoECAAQQzoGCAAQHhAHUIsRWLobYM8yaABwAHgAgAHvAogBqA-SAQUyLTEuNZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=QJjJYtqzJ4e2aabJs4AG&bih=695&biw=1349&hl=en", "https://www.google.com/search?q=unriped+tomato&tbm=isch&ved=2ahUKEwjIiITCiez4AhUIhRoKHfKoAkkQ2-cCegQIABAA&oq=unriped+tomato&gs_lcp=CgNpbWcQAzIGCAAQChAYOgQIIxAnOgUIABCABFDNCFjnYmD6amgBcAB4AIAB1QKIAdwYkgEFMi0xLjmYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=TpjJYsipE4iKavLRisgE&bih=695&biw=1349&hl=en"]
track = 0

def download_image(url, folder_name, num):

    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as f:
            f.write(reponse.content)




for query in queries:
    print("Chrome Launched successfully!!!")
    driver.get(query)
    print(f'Serching for {classes[track]}.....')
    a = input("Waiting for full load of images.....")
   
    driver.execute_script("window.scrollTo(0, 0);")

    page_html = driver.page_source
    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.findAll('div', {'class':"isv-r PNCib MSM1fd BUooTd"} )
    num_contain = len(containers)
    print(f'{num_contain} images loaded.')
    #//*[@id="islrg"]/div[1]/div[3]/a[1]/div[1]/img
    # //*[@id="islrg"]/div[1]/div[4]/a[1]/div[1]/img
    # //*[@id="islrg"]/div[1]/div[50]/div/div[1]/h2
    #//*[@id="islrg"]/div[1]/div[25]/div/div[1]/h2
    
    try:
        for i in range(1, num_contain+1):
            if i % 25 == 0:
                continue
            #//*[@id="islrg"]/div[1]/div[50]/div/div[1]/h2
            #//*[@id="islrg"]/div[1]/div[50]/div/div[1]/h2
            #//*[@id="islrg"]/div[1]/div[75]/div/div[1]/h2
            #//*[@id="islrg"]/div[1]/div[10]/a[1]/div[1]/img
            try:
                xPath = f"""//*[@id="islrg"]/div[1]/div[{i}]"""
                previmgX = f"""//*[@id="islrg"]/div[1]/div[{i}]/a[1]/div[1]/img"""
                previmgE = driver.find_element_by_xpath(previmgX)
                previmgURL = previmgE.get_attribute("src")
                driver.find_element_by_xpath(xPath).click()
            #print("preview URL", previmgURL)
            except:
                print("Can't find more images")
                continue
            #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img
            #print(xPath)


            
            start_time = time.time()
            
            while True:
                #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img
                imgElement = driver.find_element_by_xpath("""//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img""")
                imgURL = imgElement.get_attribute('src')

                if imgURL != previmgURL:
                    #print("actual URL", imgURL)
                    break

                else:
                    #making a timeout if the full res image can't be loaded
                    curr_time = time.time()

                    if curr_time - start_time < 10:
                        print("Timeout! Will download a low-res img")
                        break
            try:
                download_image(imgURL, folders[track], i)
                print(f"Downloaded element {i} out of {num_contain + 1} total. URL:{imgURL}")
                
                
            except:
                print(f"Couldn't download image {i}, continuing downloading the next one")
    except:
        continue

                   
    print("Next Query!")
    track += 1
    time.sleep(3)
    #driver.close()