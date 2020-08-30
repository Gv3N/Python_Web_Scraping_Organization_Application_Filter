# automated data parse from UUM Job list
import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup as bs
import pandas as pd

# credentials as input as different people can use this system
# username = input("Enter in your username:")
# password = input("Enter in your password:")


driver = webdriver.Chrome()
# get the url
driver.get("https://auth.uum.edu.my/nidp/idff/sso?id=3&sid=0&option=credential&sid=0&target=https://portal.uum.edu.my/")

# get the elements from the website
username_textbox = driver.find_element_by_name("Ecom_User_ID").send_keys("xxx")
password_textbox = driver.find_element_by_name("Ecom_Password").send_keys("xxx")

login_btn = driver.find_element_by_name("B1").submit()

# close pop up still in dev, need to manually trigger.
# close_pop_up = driver.find_element_by_css_selector("div[class='text-right'][style='cursor:pointer;']").click()
# close_pop_up = driver.find_element_by_xpath('//text-right[img/@src="image/closeErrorRequest.png"]').click()
# put the thread to sleep for 10 sec, will improve to wait until btn is available to click.
time.sleep(10)
# driver.manage().timeouts().implicitlyWait(10, TimeUnit.SECONDS);

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

# send current driver url to bs4 & parse all the data


def parse_content(table):
    n_columns = 0
    n_rows = 0
    column_names = []

    # Find number of rows and columns
    # we also find the column titles if we can
    for row in table.find_all('tr'):
        # n_rows += 1
        # Determine the number of rows in the table
        td_tags = row.find_all('td')
        if len(td_tags) > 0:
            n_rows += 1
        if n_columns == 0:
            # Set the number of columns for our table
            n_columns = len(td_tags)

        # Handle column names if we find them
        th_tags = row.find_all('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)
        df = pd.DataFrame(columns=columns,
                          index=range(0, n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
        columns = row.find_all('td')
        for column in columns:
            df.iat[row_marker, column_marker] = column.get_text()
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1
    return df


html_doc = driver.page_source
# driver.close()
soup = bs(html_doc, 'lxml')
table = soup.find("table", attrs={"id": "ContentPlaceHolder1_MainContent_GridView1"})
parse_content(table)

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
