# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:47:11 2021

@author: Катрина
"""

import MySQLdb # библиотека для работы с MySQL
import numpy as np # работа с массивами
import igraph # библиотека для работы с графами
import webbrowser # для открытия файла с построенным графом
from parse_latex import parse_latex

#подключение к базе данных
conn = MySQLdb.connect('localhost', 'root', 'root','biomedical_indicators',charset='utf8', 
                       use_unicode = True)
cursor = conn.cursor()

# ЗАПРОСЫ ДЛЯ ПАРСИНГА ФОРМУЛЫ
rows=cursor.execute("SELECT Latin_name, Short_name, Calculation_form_1 \
                    FROM (basic_name_indicator INNER JOIN unit_form_basic \
                    ON basic_name_indicator.idBasicName = unit_form_basic.idBasicName) \
                    INNER JOIN formula ON unit_form_basic.idFormula = formula.idFormula \
                    WHERE (idType_indicator=2) \
                    ORDER BY idUnit_form_basic;")
rows = cursor.fetchall() # получение данных из запроса

# определение массивов
base_name = [0 for i in range(len(rows))] # базовое имя
short_name = [0 for i in range(len(rows))] # короткое имя
formula_latex = [0 for i in range(len(rows))] # формула

# для каждой строки запроса
for i in range(len(rows)):
    base_name[i] = rows[i][0] # базовое имя 
    short_name[i]=rows[i][1] # короткое название
    formula_latex[i] = parse_latex(rows[i][2]) # формула
base_name = np.array(base_name) # преобразование в массив numpy (А НАДО ЛИ???)

# длинная версия имён
for i in range(len(rows)):
    for j in range(len(formula_latex[i])):
        #print(formula_latex[i][j])
        # запрос на нахождение показателя с определённой аббревиатурой
        rows_lat = cursor.execute("SELECT Latin_name\
          FROM additional_name INNER JOIN basic_name_indicator \
          ON additional_name.idBasicName = basic_name_indicator.idBasicName \
          WHERE Abbreviation_add_name = '%s'" % formula_latex[i][j])
        rows_lat = cursor.fetchall()
        if len(rows_lat) != 0:
            formula_latex[i][j] = rows_lat[0][0]
        else:
            formula_latex[i][j] = ''
    formula_latex[i] = [ind for ind in formula_latex[i] if ind!='']
        
row_all_lat = cursor.execute("SELECT Latin_name \
                             FROM basic_name_indicator \
                             ORDER BY idBasicName;;")
row_all_lat = cursor.fetchall()
all_latin_name = [0 for i in range(len(row_all_lat))]
for i in range(len(row_all_lat)):
    all_latin_name[i] = row_all_lat[i][0]
n = len(all_latin_name)
matrix_smeg = [[0 for i in range(n)]for j in range(n)]
edges_graph = []
for i in range(n):
    for j in range(len(base_name)):
        if all_latin_name[i] == base_name[j]:
            if (len(formula_latex[j]))!=0:
                for h in range(len(formula_latex[j])):
                    m = all_latin_name.index(formula_latex[j][h])
                    matrix_smeg[i][m] = 1
                    edges_graph.append((i,m))
matrix_smeg = np.array(matrix_smeg)

'''       
rows_lat1 = cursor.execute("SELECT Latin_name\
                          FROM additional_name INNER JOIN basic_name_indicator \
                          ON additional_name.idBasicName = basic_name_indicator.idBasicName \
                          WHERE Abbreviation_add_name = 'ПДД';")
rows_lat1 = cursor.fetchall()


#bas_name_formula = np.array(bas_name_formula)

for i in range(len(bas_name_formula)):
    bas_name_formula[i][1] = parse_latex(bas_name_formula[i][1])
''' 