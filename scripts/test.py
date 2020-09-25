#!/usr/bin/python3

import re
import sys
import mechanize
from bs4 import BeautifulSoup
from urllib.request import urlopen


def printTopicos(topicos):
    for t in topicos:
        print(t)


def printTextos(topico):
    for ch in bula:
        print(ch + '\n#' + bula[ch] + '\n\n')


site = 'https://bulas.medicamentos.app/medicamentos'
medicamento = 'aspirina'

br = mechanize.Browser()
br.set_handle_robots(False)

br.open(site)

br.form = list(br.forms())[0]

br['termo'] = medicamento

page = br.submit()
page = page.read()


soup = BeautifulSoup(page, 'html.parser')
tagsA = soup.find_all('a')

title = 'title="' + medicamento.lower().capitalize() + '"'
indices = [i for i, s in enumerate(tagsA) if title in str(s)]

bula_url = tagsA[indices[0]]['href']

page = urlopen(bula_url)
page = page.read()

soup = BeautifulSoup(page, 'html.parser')

tagsH4 = soup.findAll('h4')
topicos = list(map(lambda s: re.sub('</?h4>', '', str(s)), tagsH4))

bula = {}

content = soup.getText()

for i in range(len(topicos) - 1):
    ini = content.find(topicos[i])
    fim = content.find(topicos[i + 1])
    bula[topicos[i]] = content[ini + len(topicos[i]):fim]

bula[topicos[-1]] = content[fim + len(topicos[-1]):]

printTopicos(topicos)
print('\n\n')
printTextos(bula)
