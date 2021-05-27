#-------------------------------------import statements------------------------------------------------------------------------

from bs4 import BeautifulSoup
import requests
import pandas as pd
import urllib.request
import time
import json
import pymongo

#------------------------------------------------------------------------------------------------------------------------------





#------------------------------------CONNECTING TO MongoDB---------------------------------------------------------------------
client=pymongo.MongoClient("mongodb://localhost:27017")
#------------------------------------------------------------------------------------------------------------------------------





#------------------------------------Creating a CSV file-----------------------------------------------------------------------

frame=[]
upperframe=[]  
filename="NEWZSCRAPPED.csv"
f=open(filename,"w", encoding = 'utf-8')
headers="Statement,Link,Date, Source, Label, Author\n"
f.write(headers)

#-----------------------------------------------------------------------------------------------------------------------------





#-----------------------------------Function to scrape---------------------------------------------------------------------------------------------------------------------

def scrape_website(page_number):
    page_num=str(page_number)
    URL='https://www.politifact.com/factchecks/list/?page=1'
    webpage=requests.get(URL)
    soup=BeautifulSoup(webpage.text, 'html.parser')
    links=soup.find_all('li',attrs={'class':'o-listicle__item'})



    for j in links:

        Statement = j.find("div",attrs={'class':'m-statement__quote'}).text.strip()
        Link = "https://www.politifact.com"
        Link += j.find("div",attrs={'class':'m-statement__quote'}).find('a')['href'].strip()
        Date = j.find('div',attrs={'class':'m-statement__body'}).find('footer').text[-14:-1].strip()
        Author=j.find('div',attrs={'class':'m-statement__body'}).find('footer').text.strip()
        name=Author.split()
        firstname = name[1]
        lastname = name[2]
        Author = firstname + ' '+ lastname
        Source = j.find('div', attrs={'class':'m-statement__meta'}).find('a').text.strip()
        Label = j.find('div', attrs ={'class':'m-statement__content'}).find('img',attrs={'class':'c-image__original'}).get('alt').strip()
        
        frame.append((Statement,Link,Date,Source,Label,Author))
        f.write(Statement.replace(",","^")+","+Link+","+Date.replace(",","^")+","+Source.replace(",","^")+","+Label.replace(",","^")+","+Author.replace(",","^")+"\n")
    upperframe.extend(frame)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------      





#-------------------------calling the scrapping function--------------------------------------------------------

n=2
for i in range(1,n):
    scrape_website(i)
    f.close()

    # putting data into dataframe
    data=pd.DataFrame(upperframe, columns=['Statement','Link','Date','Source','Label','Author'])  
    # print(data.head())    //just to check and confirm
    
#------------------------------------------------------------------------------------------------------------------





#-----------------------------converting dataframe to dictonary---------------------------------------------------
data1= data.to_dict(orient="records")
#-----------------------------------------------------------------------------------------------------------------




#----------------------------defining the database and collection(table) name in MongoDB----------------------------

db=client["NewsArticles"]
db.Scrapnews.insert_many(data1)
#------------------------------------------------------------------------------------------------------------------




