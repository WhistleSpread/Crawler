# contents_bdwk.py
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"')   
driver = webdriver.Chrome(chrome_options=options)

wait = WebDriverWait(driver,10)
driver.get('https://wenku.baidu.com/view/77166927a5e9856a5612602c.html?rec_flag=default&sxts=1533516595558')

page = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@id='html-reader-go-more']")))
driver.execute_script('arguments[0].scrollIntoView();', page)      
nextpage = wait.until(EC.element_to_be_clickable((By.XPATH,"//span[@class='moreBtn goBtn']")))
nextpage.click()
time.sleep(2)
driver.execute_script('window.scrollTo({top:0, behavior:"smooth"})')

# contents = driver.page_source
html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
with open('./data/'+'contents', 'w', encoding='utf-8') as f:
    # f.writelines(contents)
    f.writelines(html)
    f.write('\n\n')