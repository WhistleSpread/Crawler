# contents_bdwk.py
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# options = webdriver.ChromeOptions() 
# options.add_argument('headless') 
# browser = webdriver.Chrome("./chromedriver", chrome_options=options) 
# 把上面的browser加入chrome_options参数


options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"')   
driver = webdriver.Chrome(chrome_options=options)

wait = WebDriverWait(driver,10)
driver.get('https://wenku.baidu.com/view/77166927a5e9856a5612602c.html?rec_flag=default&sxts=1533516595558')

page = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@id='html-reader-go-more']")))
driver.execute_script('arguments[0].scrollIntoView();', page)      
nextpage = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='moreBtn goBtn']")))
nextpage.click()
# top = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='crubms-wrap']")))
# driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(2)
driver.execute_script('window.scrollTo({top:0, behavior:"smooth"})')
# driver.execute_script('window.scrollTo({top:2000, behavior:"smooth"})')
# driver.execute_script('window.scrollTo({top:document.body.scrollHeight, behavior:"smooth"})')
# driver.execute_script('var q=document.documentElement.scrollTop=0') 


# target = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='btn-download']")))
# driver.execute_script('arguments[0].scrollIntoView();', target)  

for i in range(24):
	driver.execute_script('window.scrollBy(0, window.innerHeight)')
	wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ie-fix']")))

html = driver.page_source
bf1 = BeautifulSoup(html, 'lxml')

title = bf1.find_all('h1', class_='reader_ab_test with-top-banner')
bf2 = BeautifulSoup(str(title), 'lxml')
title = bf2.find('span')
title = title.get_text()
filename = title + '.txt'
print(filename)

texts_list = []
result = bf1.find_all('div', class_='ie-fix')
print('len(result) =', len(result))
print(result)
for each_result in result:
    bf3 = BeautifulSoup(str(each_result), 'lxml')
    texts = bf3.find_all('p')
    print('get one!')
    # print(texts)
    for each_text in texts:
        texts_list.append(each_text.string)
contents = ''.join(texts_list).replace('\xa0', '')
# print(contents)

with open('./data/'+filename, 'w', encoding='utf-8') as f:
    f.writelines(contents)
    f.write('\n\n')








