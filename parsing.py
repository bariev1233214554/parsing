import pandas as pd
from bs4 import BeautifulSoup
import os
import requests

url = f'https://www.film.ru/serials/soon'
r = requests.get(url)
# Ответ сайта в html
with open('film.html', 'w', encoding='utf-8') as output_file:
   output_file.write(r.text)
html_content = requests.get(url).text
soup = BeautifulSoup(r.text, 'lxml')

# Получаем количество записей па странице
entries = soup.find_all('div', class_="redesign_afisha_movie")
chislo = len(entries)
print('Записей: ',chislo)
data = []
def spisok(vid='div',cls1='redesign_afisha_movie_main',cls2='redesign_afisha_movie_main_serial',par1='Название',par2='"Сезон / эпизод"' ):
# Название и эпизод
   for entry in entries:
      td_film_details = entry.find(vid, class_= cls1)
      film_name = td_film_details.find('strong').text
      release_date = entry.find(vid, class_=cls2).text
      data.append({par1: film_name, par2: release_date})
   return data
data = spisok()
dat = pd.DataFrame(data)
print(dat)
df = pd.DataFrame(dat)
df.to_excel("New_anime.xlsx")
#Отправка данных в телеграмм бот
def send_file_via_telegram(token='', chat_id=, file_path="):
   url = f"https://api.telegram.org/bot{token}/sendDocument"
   with open(file_path, 'rb') as file:
      files = {
         'document': (
            os.path.basename(file_path),  # имя файла, которое увидит получатель
            file,  # файловый объект
            'application/octet-stream'  # MIME‑тип (универсальный)
                      )
      }
      data = {'chat_id': chat_id}
      response = requests.post(url, files=files, data=data, timeout=30)
      return response.json()
result = send_file_via_telegram()
print(result)
