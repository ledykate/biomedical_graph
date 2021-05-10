# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:47:11 2021

@author: Катрина
"""

import MySQLdb # библиотека для работы с MySQL
#import numpy as np # работа с массивами
import igraph # библиотека для работы с графами
import webbrowser # для открытия файла с построенным графом
from parse_latex import parse_latex

#подключение к базе данных
conn = MySQLdb.connect('localhost', 'root', 'root','biomedical_indicators',charset='utf8', 
                       use_unicode = True)
cursor = conn.cursor()

vertices_label = [] # названия вершин
color_vs = [] # цвета вершин
####### ПОКАЗАТЕЛИ И ФОРУМАЛА
rows=cursor.execute("SELECT Latin_name, Calculation_form_1 \
                    FROM (basic_name_indicator INNER JOIN unit_form_basic \
                    ON basic_name_indicator.idBasicName = unit_form_basic.idBasicName) \
                    INNER JOIN formula ON unit_form_basic.idFormula = formula.idFormula \
                    WHERE (idType_indicator=2) \
                    ORDER BY idUnit_form_basic;")
rows = cursor.fetchall() # получение данных из запроса

# определение массивов
base_name = [] # базовое имя
formula_latex = [] # формула
##### РАСПРЕДЕЛЕНИЕ ПО МАССИВАМ
# для каждой строки запроса
for i in range(len(rows)):
    base_name.append(rows[i][0]) # базовое имя 
    formula_latex.append(parse_latex(rows[i][1])) # формула

##### ПОИСК Латинского названия по аббревиатуре
for i in range(len(rows)):
    for j in range(len(formula_latex[i])):
        # запрос на нахождение показателя с определённой аббревиатурой
        rows_lat = cursor.execute("SELECT Latin_name\
          FROM additional_name INNER JOIN basic_name_indicator \
          ON additional_name.idBasicName = basic_name_indicator.idBasicName \
          WHERE Abbreviation_add_name = '%s'" % formula_latex[i][j])
        rows_lat = cursor.fetchall() # получение данных из запроса
        if len(rows_lat) != 0: # если запрос не пустой
            formula_latex[i][j] = rows_lat[0][0] # заменяем аббревиатуру на латинское название
        else:
            formula_latex[i][j] = '' # если не нашёл, то пустой 
    # оставляем только не пустые значения
    formula_latex[i] = [ind for ind in formula_latex[i] if ind!='']
        
# все латинские имена
row_all_lat = cursor.execute("SELECT Latin_name \
                             FROM basic_name_indicator \
                             ORDER BY idBasicName;;")
row_all_lat = cursor.fetchall()

all_latin_name = [] # массив с латинскими именами
# добавление в массив всех элементов запроса
for i in range(len(row_all_lat)):
    all_latin_name.append(row_all_lat[i][0])
    color_vs.append([0,0,1]) # цвет у вершин голубой
n = len(all_latin_name) # количество покавсех показателей

edges_graph = [] # массив с рёбрами (кортежы)
for i in range(n): # для всех показателей
    for j in range(len(base_name)): # для показателей, которые имеют формулу
        if all_latin_name[i] == base_name[j]: # если совпадают
            # формула не пустая (в БД есть показатели из формулы)
            if (len(formula_latex[j]))!=0: 
                for h in range(len(formula_latex[j])): # для каждого аргумента
                    # находим индекс показателя
                    m = all_latin_name.index(formula_latex[j][h]) 
                    edges_graph.append((i,m)) # добавляем ребро

vertices_label += all_latin_name # добавляем в подписи к вершинам

##### ПОКАЗАТЕЛИ, ФОРМИРУЕМЫЕ ПО МЕТОДИКЕ--------------------------------------
# запрос, которые выводит всю таблицу formed_idicator_method, но
# вместо id показатели и методики выводит латинское название показателя
# и название методики на русском языке
row_meth_ind = cursor.execute("SELECT Latin_name, Name_method_Russian \
                              FROM (formed_idicator_method LEFT JOIN basic_name_indicator \
                              ON formed_idicator_method.idBasicName = basic_name_indicator.idBasicName) \
                              LEFT JOIN method ON formed_idicator_method.idMethod = method.idMethod \
                              ORDER BY formed_idicator_method.idFormed_indicator;")
row_meth_ind = cursor.fetchall()

formed_ind = [] # создание массива с показателями
formed_meth = [] # создание массива с методиками
for i in range(len(row_meth_ind)): # проходимя по строкам запроса
    formed_ind.append(row_meth_ind[i][0])
    if row_meth_ind[i][1] == None: # если ещё не добавлена методика у показателя
        formed_meth.append('') # пустой
    else: # иначе
        formed_meth.append(row_meth_ind[i][1])  # добавляем
        
# добавляем уникальные (не повторяющиеся) названия методик
vertices_label += list(set(formed_meth)) 
empty = ''
# удаляем пустые значения (если есть)
while empty in vertices_label: vertices_label.remove(empty) 

for i in range(n): # проходимся по всем показателям (см.ранее)
    for j in range(len(formed_ind)): # показатели, которые сформерованы по методике
        if vertices_label[i] == formed_ind[j]: # совпадают
            met = formed_meth[j] # ищем соответвующую методику
            if met != '': # если не пустая
                # добавялем ребро
                edges_graph.append((i,vertices_label.index(met)))

#### МЕТОДИКИ И ОБОРУДОВАНИЕ, НА КОТОРОМ ОНИ ИЗМЕРЯЮТСЯ------------------------  
# запрос таблицы unit_method_equip, но выводятся русское название методики
# и название оборудования
rows_met_eq = cursor.execute("SELECT Name_method_Russian, Name_equipment \
                             FROM (unit_method_equip INNER JOIN method \
                             ON unit_method_equip.idMethod = method.idMethod) \
                             INNER JOIN equipment ON unit_method_equip.idEquipment = equipment.idEquipment;")
rows_met_eq = cursor.fetchall()

met = [] # создание массива с методиками
eq = [] # создание массива с оборудованием
for i in range(len(rows_met_eq)): # заполнение данных по запросу
    met.append(rows_met_eq[i][0]) # методика
    eq.append(rows_met_eq[i][1]) # оборудование

# добавление методик, которые ещё не связаны с показателями
for i in range(n,len(vertices_label)): # не влючая сами показатели!
    color_vs.append([0,1,0]) # цвет методик зелёный
    for j in range(len(met)): 
        if vertices_label[i]!=met[j]: # если ещё такой не было
            vertices_label.append(met[j]) # добавляем
            color_vs.append([0,1,0]) # зелёный

vertices_label += list(set(eq)) # названия оборудования в список с вершинами

for i in range(len(list(set(eq)))): # цвет для вершин с оборудованием
    color_vs.append([1,1,0]) # жёлтый
for i in range(n,len(vertices_label)): # проходимся по массиву не влючая показатели!
    for j in range(len(met)):
        if vertices_label[i]==met[j]: # соответствуют
            e = eq[j] # оборудование
            edges_graph.append((i,vertices_label.index(e))) # добавляем ребро

##### ПОКАЗАТЕЛИ И СИСТЕМЫ ОРГАНИЗМА, К КОТОРЫМ ОТНОСЯТСЯ----------------------
# Запрос для вывода латинским имён показателей и названия системы
row_ind_sys = cursor.execute("SELECT Latin_name, Name_systems \
                             FROM basic_name_indicator INNER JOIN systems_indicator \
                             ON basic_name_indicator.idGroupSystems = systems_indicator.idGroupSystems;")
row_ind_sys = cursor.fetchall()

indic = [] # создаём массив с показателями
systems = [] # создаём массив с системами
# заполняем массивы по запросу
for i in range(len(row_ind_sys)):
    indic.append(row_ind_sys[i][0])
    systems.append(row_ind_sys[i][1])
    
vertices_label += list(set(systems)) # добавляем названия 
for i in range(n): # проходимся по показателям
    for j in range(len(indic)): # по показателям из запроса
        if vertices_label[i]==indic[j]: # совпадают
            sys = systems[j] # находим соотвествующую системы
            color_vs.append([1,0,0]) # задаём цвет - красный
            edges_graph.append((i,vertices_label.index(sys))) # добавляем ребро

### ОТОБРАЖЕНИЕ В ВИДЕ НАПРАВЕЛЕННОГО ГРАФА
#####-----------------
# редактирование подписей к вершинам по разделителю
for i in range(len(vertices_label)):
    text_label = vertices_label[i]
    vertices_label[i] = text_label.replace(" ", "\n") # расзделитель пробел
for i in range(len(vertices_label)):
    text_label = vertices_label[i]
    vertices_label[i] = text_label.replace("-", "\n") # разделитель дефис 
g = igraph.Graph(directed = True) # напревленный граф
g.add_vertices(len(vertices_label)) # количество вершин
g.vs["label"] = vertices_label # подписи вершин
g.vs['color'] = color_vs # цвета вершин
g.vs["size"] = 60 # размер вершин
g.vs["label_size"] = 10 # размер подписи
g.add_edges(edges_graph) # добавление рёбер
g.es["width"] = 1.2 # ширина ребра
layout = g.layout_reingold_tilford_circular() # стиль графа в общем
# построение графа
igraph.plot(g, "test_indic.png", layout = layout,bbox = (800,800),margin = (35,80,35,80))
webbrowser.open_new_tab("test_indic.png") #открытие созданного файла