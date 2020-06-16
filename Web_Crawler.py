from bs4 import BeautifulSoup
import requests
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials





scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("News").sheet1
sheet.delete_rows(2,200)





page = 1
while page != 0:
    url = 'https://bangaloremirror.indiatimes.com/bangalore/crime/articlelist/msid-20970789,curpg-' + str(page) + '.cms'

    code = requests.get(url)
    soup = BeautifulSoup(code.text, 'lxml')

    links = soup.find('div', {'class': 'ipl_lnews containerDiv clearfix'}).findAll('a', href=re.compile(
        "(/bangalore/crime/)+([A-Za-z0-9_.()])"))
    for link in links:
        ab = 2
        Headline = link.text
        img = link.img.get('data-src')
        img_url = 'https://bangaloremirror.indiatimes.com' + img
        Link = 'https://bangaloremirror.indiatimes.com' + link['href']
        url = Link
        code = requests.get(url)
        soup = BeautifulSoup(code.text, 'lxml')
        news = soup.find('div', {'class': 'Normal'})

        extra1 = news.script
        extra1.decompose()
        extra2 = news.script
        extra2.decompose()
        extra3 = news.script
        extra3.decompose()

        news_discription = news.text

        view_more = '\n                        View More\n                        '
        if Headline == 'Next' or Headline == 'Prev' or Headline == view_more:
            continue

        insertRow = [Headline, Link, img_url, news_discription]
        sheet.insert_row(insertRow, ab)
        ab = ab + 1
    page = page + 1
