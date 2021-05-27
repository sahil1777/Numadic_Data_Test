#-------------------------------Import statements---------------------------------------------------------------------
from bs4 import BeautifulSoup 
import requests
import pandas as pd
import urllib.request
import time

#----------------------------------------------------------------------------------------------------------------------





#-------------------------------Creating CSV File------------------------------------------------------------------------
frame=[]
filename="NEWZSCRAPPED.csv"
f=open(filename,"w", encoding = 'utf-8')
headers="Statement,Link,Date, Source, Label\n"
f.write(headers)
#--------------------------------------------------------------------------------------------------------------------------







#-------------------------------Scrapping function----------------------------------------------------------------------------------------------------

def scrape_website(page_number):
    page_num=str(page_number)
    URL='https://www.politifact.com/factchecks/list/?page=1'  #website to be scraped
    webpage=requests.get(URL)
    soup=BeautifulSoup(webpage.text, 'html.parser')
    links=soup.find_all('li',attrs={'class':'o-listicle__item'})

    for j in links:
        Statement = j.find("div",attrs={'class':'m-statement__quote'}).text.strip()
        
        Link = "https://www.politifact.com"
        Link += j.find("div",attrs={'class':'m-statement__quote'}).find('a')['href'].strip()
        Date = j.find('div',attrs={'class':'m-statement__body'}).find('footer').text[-14:-1].strip()
        Source = j.find('div', attrs={'class':'m-statement__meta'}).find('a').text.strip()
        Label = j.find('div', attrs ={'class':'m-statement__content'}).find('img',attrs={'class':'c-image__original'}).get('alt').strip()
        frame.append((Statement,Link,Date,Source,Label))
        # writing into CSV
        f.write(Statement.replace(",","^")+","+Link+","+Date.replace(",","^")+","+Source.replace(",","^")+","+Label.replace(",","^")+"\n")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------






#--------------------------------calling scrapping function-----------------------------------------------
n=2
for i in range(1,n):
    scrape_website(i)
#---------------------------------------------------------------------------------------------------------