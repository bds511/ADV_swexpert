import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from decouple import config
import requests
import urllib.request
from shutil import copyfile
from bs4 import BeautifulSoup as bs
import time
import random

id=config('ID')
password = config('PASSWORD')

class swexpert:
    
    def __init__(self):
        if not os.path.exists("SW_Expert"):
            os.mkdir("SW_Expert")
        chrome_options = Options()
        #browser = webdriver.Firefox()
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.url_dict={}
        print("브라우저 오픈")


        
    
    def login(self,id=id, password=password):
        self.browser.get("https://swexpertacademy.com/main/identity/anonymous/loginPage.do")
        self.browser.implicitly_wait(1)

        self.browser.find_element_by_id("id").send_keys(id)
        self.browser.find_element_by_id("pwd").send_keys(password)
        self.browser.implicitly_wait(1)
        self.browser.execute_script('loginSecurityPledge()')
        print("로그인 완료")


    def get_url_dict(self):
        for i in range(1,2):
            res = requests.get(
                'https://swexpertacademy.com/main/code/problem/problemList.do?problemTitle=&orderBy=FIRST_REG_DATETIME&select-1=&pageSize=10&pageIndex=' + str(
                    i))
            soup = bs(res.content)

            for j in soup.find(class_="widget-list").find_all(class_="widget-box-sub"):
                self.url_dict.update({j.find(class_='week_num').text.split(".")[0]:
                                     str(j.find(class_='week_text').a).split("fn_move_page('")[1].split("');")[0]})
        print("리스트 다운 완료")

    def get_url(self):
        for key,val in self.url_dict.items():
            my_path = "SW_Expert\\" + key
            if not os.path.exists(my_path):
                time.sleep(random.random()*0)
                self.get_problem("https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId="+val)

    def get_problem(self,url):
        self.browser.get(url)

        title = self.browser.find_element_by_class_name("problem_title").text.split(".")[0]

        my_path = "SW_Expert\\" + title

        if not os.path.exists(my_path): ##폴더가 없을때만 크롤링 실행
            os.mkdir(my_path)

            text = self.browser.find_element_by_class_name("box4")
            html = self.browser.execute_script("return arguments[0].outerHTML;", text).replace("/main/","https://swexpertacademy.com/main/")
            html = """<html lang="ko">
<head><meta charset="utf-8"></head>
""" + html + f'<br><strong>[출처]</strong> : {url} </html>'
            with open(my_path + "\\problem.html", 'w', encoding='utf-8') as text_file:
                text_file.write(html)

            text = self.browser.find_element_by_class_name("box4").text

            with open(my_path + "\\problem.txt", 'w', encoding='utf-8') as text_file:
                text_file.write(text)

            input_path = self.browser.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/div[7]/div/div[3]/div[1]/div[1]/div/a[2]").get_attribute('href')
            urllib.request.urlretrieve(input_path, my_path + '\\input.txt')

            output_path = self.browser.find_element_by_xpath(
                "/html/body/div[4]/div[2]/div/div[7]/div/div[3]/div[2]/div/div/a[2]").get_attribute('href')
            urllib.request.urlretrieve(output_path, my_path + '\\output.txt')

            copyfile("Templates\\checker.py", my_path + "\\checker.py")
            copyfile("Templates\\problem.py", my_path + "\\problem.py")
            with open(my_path + "\\checker.py",'a',encoding='utf-8') as text_file:
                text_file.write('    print("문제출처 : '+url+'")')
            print(title+"다운완료")


        



url="https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWvzGUKKPVwDFASy&categoryId=AWvzGUKKPVwDFASy&categoryType=CODE"

browser= swexpert()
browser.login()
browser.get_url_dict()
browser.get_url()

#browser.get_problem(url)

