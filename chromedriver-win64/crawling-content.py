from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote_plus as qp
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def user_data():
    global username, userpw, hashTag, N, M
    username = '' # 아이디
    userpw = '' # 패스워드
    hashTag = input("검색어를 입력하세요 : ") # 검색 태그
    N = input("스크롤 횟수를 지정하세요 : ")
    M = input("다운받을 이미지 개수를 정하세요 : ")

    hashTag = str(hashTag)
    N = int(N)    
    M = int(M)

def url_setting():
    loginUrl = 'https://www.instagram.com/accounts/login/'
    return loginUrl

def login(driver):
    driver.get(url_setting())

    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(userpw)

    driver.find_element(By.NAME, 'password').send_keys(Keys.ENTER)
    driver.implicitly_wait(5)

    driver.find_element(By.CLASS_NAME, '_a9--._a9_1').click()
    driver.implicitly_wait(5)

def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    #Get Content Address
    imglist = []
    for i in range(0, N):
        insta = soup.select('._aabd._aa8k._al3l')

        for i in insta:
            print('https://www.instagram.com' + i.a['href'])
            imgUrl = i.select_one('._aagv').img['src']
            imglist.append(imgUrl)
            imglist = list(set(imglist))
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            insta = soup.select('._aabd._aa8k._al3l')

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(3)

    #Save images to Computer
    n = 0
    for i in range(0, M):
        try:
            image_url = imglist[n]
        
            with urlopen(image_url) as f:
                with open('./img/' + hashTag + str(n) + '.jpg', 'wb') as h:
                    img = f.read()
                    h.write(img)

                n += 1
        
        except: 
            print("강제 종료: 요구사항보다 게시물 부족")
            break

    print(f"{n}개 항목 다운로드 완료.")

def searching(driver):
    #Click Searching box to Open Input Bar / Q: why used try-catch? A: because Responsive website UI
    try:
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div/div[2]/span/div/a').send_keys(Keys.ENTER)
    except:
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[2]/span/div/a').send_keys(Keys.ENTER)
    driver.implicitly_wait(5)

    try:
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div/div/div/input').send_keys(hashTag)
    except:
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div/div/input').send_keys(hashTag)
    driver.implicitly_wait(5)

    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div/a[1]').send_keys(Keys.ENTER)
    except:
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/a[1]').send_keys(Keys.ENTER)
    time.sleep(6)

def engine():
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    login(driver)
    searching(driver)
    get_content(driver)
    driver.close()

#Start on Here
user_data()
engine()