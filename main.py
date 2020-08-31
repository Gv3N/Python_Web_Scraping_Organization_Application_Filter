# automated data parse from UUM Job list

import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import pandas as pd

# credentials as input as different people can use this system
username = input("Enter in your username:")
password = input("Enter in your password:")


driver = webdriver.Chrome()
# get the url
driver.get("https://auth.uum.edu.my/nidp/idff/sso?id=3&sid=0&option=credential&sid=0&target=https://portal.uum.edu.my/")

# get the elements from the website
username_textbox = driver.find_element_by_name("Ecom_User_ID").send_keys(username)
password_textbox = driver.find_element_by_name("Ecom_Password").send_keys(password)

login_btn = driver.find_element_by_name("B1").submit()

# close pop up still in dev, need to manually trigger.
# close_pop_up = driver.find_element_by_css_selector("div[class='text-right'][style='cursor:pointer;']").click()
# close_pop_up = driver.find_element_by_xpath('//text-right[img/@src="image/closeErrorRequest.png"]').click()
# put the thread to sleep for 10 sec, will improve to wait until btn is available to click.
time.sleep(10)
# driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);
close_pop = driver.find_element_by_xpath("/html/body/form/div[6]/div[3]/div/div[1]/img").click()
academic_btn = driver.find_element_by_id("btn-academic").click()
practicum_placement = driver.find_element_by_link_text("Practicum Placement").click()

# now drop down option comes to play
# select class id for states dropdown menu
select_state = Select(driver.find_element_by_id('ContentPlaceHolder1_MainContent_ddlnegeri'))
# select Kedah
# for looping use <index> for <02> same goes for city
select_state.select_by_value('02')

# select class id for city dropdown menu
select_city = Select(driver.find_element_by_id('ContentPlaceHolder1_MainContent_ddlbandar'))
# select Alor Setar
select_city.select_by_value('0202')
time.sleep(5)


# References
# id state dropdown => ContentPlaceHolder1_MainContent_ddlnegeri
# id city drop down => ContentPlaceHolder1_MainContent_ddlbandar
# testing kedah, id=[02] -> alor setar, id=[0202] -> 1020 rows, 55 pages
# url for the table, 'https://portal5.uum.edu.my/webasis/practis/student/orga_list.aspx'
# Part 1 done-----------------------------------------------------------------------------------------------------------

# send current driver url to bs4 & parse all the data
html_doc = driver.page_source

soup = bs(html_doc, 'lxml')
table = soup.find("table", attrs={"id": "ContentPlaceHolder1_MainContent_GridView1"})
table_rows = table.find_all("tr")
driver.close()

# get all the heading of lists
# get header of table
headings = []
for th in table_rows[0].find_all("th"):
    headings.append(th.get_text())
# print(headings)
# print(table_data)

# get all the rows of table
table_data = []
limit = 21  # create limit to rows per page as there is excess rows, there will be one empty row from the header.
index = 0  # index counter
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.get_text().strip('\n, " "') for tr in td]
    # print(row)
    table_data.append(row)
    index += 1
    if index == limit:
        break
    # print(table_data)

# convert lists into dataframe
df = pd.DataFrame(table_data, columns=headings)
# print(df)
# convert into excel
df.to_csv(r'C:\Users\bakta\Desktop\test cvs\UUMTestzone.csv', index=False)
print("data have been converted to excel")


# only part left is automation for the rest of options in dropdown menu n navigation of pages
# suggestion/ideas
# for looping https://stackoverflow.com/questions/58203002/scrape-table-from-each-option-in-drop-down-menu-python can
# use some of the algo like data['stat]=i etc so we can store the value first then call them as index however for the
# cities it will be hard to get all the index - need to get state by state for the table length we can scrap href
# link into a dataframe/ dict{} then we ran loop to check if there is another page or grater number than current num
# basically can use {find max loop}

# ref
# https://stackoverflow.com/questions/61162794/scrape-each-table-from-drop-down-menu-python?rq=1
# https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup
# https://stackoverflow.com/questions/61162794/scrape-each-table-from-drop-down-menu-python?rq=1
# https://stackoverflow.com/questions/58203002/scrape-table-from-each-option-in-drop-down-menu-python
