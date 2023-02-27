#Устанавливаем библиотеки beautifulsoup4, urllib, xlsxwriter и подключаем их
import xlsxwriter
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
import re

page = 1  #Нулевая страница

URL1 = 'https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&only_with_salary=true&text=python&page=0'

URL2 = 'https://hh.ru/search/vacancy?area=113&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&only_with_salary=true&text=python&page='+str(page) #url сайта

ua = UserAgent()

headers = {
  'Host': 'hh.ru',
  'User-Agent': str(ua.chrome),
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive'
}

result1 = requests.get(f'{URL1}&page={page}', headers=headers) # скачиваем html-страницу
soup1 = BeautifulSoup (result1.text,'html.parser')#Считываем html страницу

name = soup1.find_all("h3",{"data-qa":"bloko-header-3", "class":"bloko-header-section-3"}) # берем название вакансии

salary = soup1.find_all("span", {"data-qa":"vacancy-serp__vacancy-compensation","class":"bloko-header-section-3"}) # берем какую зарплату будут получать

company = soup1.find_all("a", {"class": "bloko-link bloko-link_kind-tertiary", "data-qa": "vacancy-serp__vacancy-employer"}) # берем название компании

city = soup1.find_all("div", {"class": "bloko-text", "data-qa": "vacancy-serp__vacancy-address"}) # берем город

link = soup1.find_all('a', attrs={'href': re.compile("^https://hh.ru/vacancy/")})

print("Страница  1")

while True:
  
  result2 = requests.get(f'{URL2}&page={page}', headers=headers) #скачиваем html-страницу
  soup2 = BeautifulSoup (result2.text,'html.parser')#Считываем html страницу

  name += soup2.find_all("h3",{"data-qa":"bloko-header-3", "class":"bloko-header-section-3"}) #берем название вакансии

  salary += soup2.find_all("span", {"data-qa":"vacancy-serp__vacancy-compensation","class":"bloko-header-section-3"}) #берем какую зарплату будут получать
  salarycheck = soup2.find_all("span", {"data-qa":"vacancy-serp__vacancy-compensation","class":"bloko-header-section-3"}) #берем какую зарплату будут получать

  company += soup2.find_all("a", {"class": "bloko-link bloko-link_kind-tertiary", "data-qa": "vacancy-serp__vacancy-employer"}) # берем название компании

  city += soup2.find_all("div", {"class": "bloko-text", "data-qa": "vacancy-serp__vacancy-address"}) #берем город

  link += soup2.find_all('a', attrs={'href': re.compile("^https://hh.ru/vacancy/")}) #берем ссылки на вакансии

  #for item in range(len(salary)):
    #print(name[item].text + '  '+ salary[item].text+'  '+company[item].text+'  '+city[item].text) #выводим полученный данные на консоль
    
  if (len(salarycheck)): 
      page += 1  #переходим к следующей странице
      print("Страница  "+str(page))
  elif (len(salarycheck) == 0):#если страницы закончились
      break  #прерываем цикл
      print("Страницы закончились")






workbook = xlsxwriter.Workbook('write_list.xlsx') #создание excel файла
worksheet = workbook.add_worksheet()

for i in range(len(salary)):
    worksheet.write(i, 0, name[i].text) # запись название вакансии 

for i in range(len(salary)):
    worksheet.write(i, 1, salary[i].text) # запись зарплаты

for i in range(len(company)):
    worksheet.write(i, 2, company[i].text) # запись название компании

for i in range(len(link)):
    worksheet.write(i, 2, link[i].get('href'))

new_city = city

for item in range(len(city)):
  new_city[item] = city[item].text
  new_city[item] = new_city[item].split(',', 1)[0]


for i in range(len(new_city)):
    worksheet.write(i, 3, new_city[i]) # запись города

workbook.close()

