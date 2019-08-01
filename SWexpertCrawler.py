import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from decouple import config
import requests
import urllib.request

def download(id,password,url):
    if not os.path.exists("SW_Expert"):
        os.mkdir("SW_Expert")

    chrome_options = Options()

    #browser = webdriver.Firefox()

    browser = webdriver.Chrome(chrome_options=chrome_options)


    browser.get("https://swexpertacademy.com/main/identity/anonymous/loginPage.do")
    browser.implicitly_wait(1)


    browser.find_element_by_id("id").send_keys(id)
    browser.find_element_by_id("pwd").send_keys(password)
    browser.implicitly_wait(1)
    browser.execute_script('loginSecurityPledge()')

    browser.get(url)

    title=browser.find_element_by_class_name("problem_title").text.split(".")[0]

    my_path="SW_Expert\\"+title

    if not os.path.exists(my_path):
        os.mkdir(my_path)

    text=browser.find_element_by_class_name("box4").text

    with open(my_path+"\\problem.txt",'w') as text_file:
        text_file.write(text)


    input_path=browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[7]/div/div[3]/div[1]/div[1]/div/a[2]").get_attribute('href')
    urllib.request.urlretrieve(input_path, my_path+'\\input.txt')

    output_path= browser.find_element_by_xpath("/html/body/div[4]/div[2]/div/div[7]/div/div[3]/div[2]/div/div/a[2]").get_attribute('href')
    urllib.request.urlretrieve(output_path, my_path+'\\output.txt')

    text="""import sys
    sys.stdin=open('input.txt','r')
    """
    with open(my_path+"\\"+title+".py",'w') as text_file:
        text_file.write(text)

id=config('ID')
password = config('PASSWORD')
url="https://swexpertacademy.com/main/code/problem/problemDetail.do?contestProbId=AWsBQpPqMNMDFARG&categoryId=AWsBQpPqMNMDFARG&categoryType=CODE"

download(id,password,url)
print("다운완료")