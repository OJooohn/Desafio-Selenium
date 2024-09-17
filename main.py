# pip install selenium
import itertools
from time import sleep
import pandas as pd

from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://www.zoom.com.br/')

from selenium.webdriver.common.by import By
search_area = driver.find_element(By.CLASS_NAME, 'SearchRegion_searchRegion__Z9Y6c')
input_search = search_area.find_element(By.TAG_NAME, 'input')

from selenium.webdriver.common.keys import Keys
input_search.send_keys('notebook')
search_btn = search_area.find_element(By.TAG_NAME, 'button')
search_btn.click()

def changeFilter(filter: str):
    from selenium.webdriver.support.select import Select
    search_filter = driver.find_element(By.CLASS_NAME, 'SortBy_SortBySelect__o3gVE')
    select = Select(search_filter.find_element(By.XPATH, '//*[@id="orderBy"]'))
    select.select_by_visible_text(filter)

lista_itens_maior_preco = []
changeFilter('Menor preço')

for i in range(1, 4):
    if i > 1:
        page_selector = driver.find_element(By.XPATH, '//ul[@class="Paginator_paginator__Jmw5q"]')
        page_number = page_selector.find_elements(By.TAG_NAME, 'li')

        scroll_to = driver.find_element(By.CLASS_NAME, 'Paginator_paginator__Jmw5q')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", scroll_to)

        sleep(2)
        page_number[i].click()

    sleep(3)
    item_boxs = driver.find_elements(By.CLASS_NAME, 'Hits_ProductCard__Bonl_')
    for item in item_boxs:
        item_name = item.find_element(By.TAG_NAME, 'h2').text
        lista_itens_maior_preco.append(item_name)

    if i == 3:
        page_selector = driver.find_element(By.XPATH, '//ul[@class="Paginator_paginator__Jmw5q"]')
        page_number = page_selector.find_elements(By.TAG_NAME, 'li')

        scroll_to = driver.find_element(By.CLASS_NAME, 'Paginator_paginator__Jmw5q')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", scroll_to)

        sleep(2)
        page_number[1].click()

sleep(2)
lista_itens_menor_preco = []
changeFilter('Maior preço')

for i in range(1, 4):
    if i > 1:
        page_selector = driver.find_element(By.XPATH, '//ul[@class="Paginator_paginator__Jmw5q"]')
        page_number = page_selector.find_elements(By.TAG_NAME, 'li')

        scroll_to = driver.find_element(By.CLASS_NAME, 'Paginator_paginator__Jmw5q')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", scroll_to)

        sleep(2)
        page_number[i].click()

    sleep(3)
    item_boxs = driver.find_elements(By.CLASS_NAME, 'Hits_ProductCard__Bonl_')
    for item in item_boxs:
        item_name = item.find_element(By.TAG_NAME, 'h2').text
        lista_itens_menor_preco.append(item_name)

    if i == 3:
        page_selector = driver.find_element(By.XPATH, '//ul[@class="Paginator_paginator__Jmw5q"]')
        page_number = page_selector.find_elements(By.TAG_NAME, 'li')

        scroll_to = driver.find_element(By.CLASS_NAME, 'Paginator_paginator__Jmw5q')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", scroll_to)

        sleep(2)
        page_number[1].click()

sleep(2)
lista_itens_melhor_avaliado = []
changeFilter('Melhor avaliado')
for i in range(1, 4):
    if i > 1:
        page_selector = driver.find_element(By.XPATH, '//ul[@class="Paginator_paginator__Jmw5q"]')
        page_number = page_selector.find_elements(By.TAG_NAME, 'li')

        scroll_to = driver.find_element(By.CLASS_NAME, 'Paginator_paginator__Jmw5q')
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", scroll_to)

        sleep(2)
        page_number[i].click()

    sleep(3)
    item_boxs = driver.find_elements(By.CLASS_NAME, 'Hits_ProductCard__Bonl_')
    for item in item_boxs:
        item_name = item.find_element(By.TAG_NAME, 'h2').text
        lista_itens_melhor_avaliado.append(item_name)

# dataframe1 = pd.DataFrame(lista_itens_maior_preco, columns=['Nome'])
# dataframe1.to_csv('itens_maior_preco.csv', index=False)

# dataframe2 = pd.DataFrame(lista_itens_menor_preco, columns=['Nome'])
# dataframe2.to_csv('itens_menor_preco.csv', index=False)

# dataframe3 = pd.DataFrame(lista_itens_melhor_avaliado, columns=['Nome'])
# dataframe3.to_csv('itens_melhor_avaliado.csv', index=False)

lista = list(set(itertools.chain(lista_itens_maior_preco, lista_itens_menor_preco, lista_itens_melhor_avaliado)))

lista_nome_quant = []
for item in lista:
    quant = lista_itens_menor_preco.count(item) + lista_itens_maior_preco.count(item) + lista_itens_melhor_avaliado.count(item)
    lista_nome_quant.append((item, quant))

lista_nome_quant.sort(key=lambda x: x[1], reverse=True)
itens_relevantes = lista_nome_quant[:10]
for item in lista_nome_quant:
    print(f'Nome: {item[0]}, Quantidade: {item[1]}')

nomes_itens_relevantes = []
for item in itens_relevantes:
    if item[1] > 1:
        # item[0] -> nome
        nomes_itens_relevantes.append(item[0])

dataframe = pd.DataFrame(nomes_itens_relevantes, columns=['Nome'])
dataframe.to_csv('itens_relevantes.csv', index=False)

sleep(1)
driver.close()