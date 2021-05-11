# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:25:05 2021

@author: Катрина
"""

import MySQLdb # библиотека для работы с MySQL
import numpy as np # работа с массивами
import igraph # библиотека для работы с графами
import webbrowser # для открытия файла с построенным графом
import sys
import os
#import numpy as np # работа с массивамии
from parse_latex import parse_latex

#библиотека по работе с изображениями PIL (pillow)
from PIL import Image, ImageDraw, ImageQt, ImageEnhance, ImageFilter
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox, QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt


class Main(QMainWindow): #класс, где храняться все действия
    def __init__(self): #служебная функция инициализации,загрузка окна
        QMainWindow.__init__(self)
        loadUi("biomedical_interface.ui",self) #файл с расположение с дизайном
        self.setWindowTitle('Графовые модели')
        self.conn = MySQLdb.connect('localhost', 'root', 'root','biomedical_indicators',charset='utf8', 
                       use_unicode = True)
        self.cursor = self.conn.cursor()
        self.setWindowIcon(QIcon('icon.png'))
        #передвигать изображение
        lay = QVBoxLayout(self.scrollAreaWidgetContents)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.img)
        self.imageScrollArea.setWidgetResizable(True)
        self.img.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        
        self.image = None #изображение (pillow)
        self.photo = None #изображение в виджите (pixmap)
        
        rows = self.cursor.execute("SELECT Name_language FROM language_add_indicator;")
        rows = self.cursor.fetchall() # получение данных из запроса
        L = [0 for i in range(len(rows))]
        for i in range(len(rows)):
            L[i] = rows[i][0]
        L.insert(0,'Латинские названия')
        self.language_indicator.addItems(L)
        
        self.pushButton_update.clicked.connect(self.update_graph)
        self.ScrollBar_big.valueChanged.connect(self.big) #увелечение изображения 
        self.ScrollBar_small.valueChanged.connect(self.small) #уменьшение изображения
        self.saveas_graph.triggered.connect(self.saveas_file) #сохранить/сохранить как
        
        self.vertices_label = [] # названия вершин
        self.color_vs = [] # цвета вершин
        ####### ПОКАЗАТЕЛИ И ФОРУМАЛА
        rows = self.cursor.execute("SELECT Latin_name, Calculation_form_1 \
                            FROM (basic_name_indicator INNER JOIN unit_form_basic \
                            ON basic_name_indicator.idBasicName = unit_form_basic.idBasicName) \
                            INNER JOIN formula ON unit_form_basic.idFormula = formula.idFormula \
                            WHERE (idType_indicator=2) \
                            ORDER BY idUnit_form_basic;")
        rows = self.cursor.fetchall() # получение данных из запроса
        
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
                rows_lat = self.cursor.execute("SELECT Latin_name\
                  FROM additional_name INNER JOIN basic_name_indicator \
                  ON additional_name.idBasicName = basic_name_indicator.idBasicName \
                  WHERE Abbreviation_add_name = '%s'" % formula_latex[i][j])
                rows_lat = self.cursor.fetchall() # получение данных из запроса
                if len(rows_lat) != 0: # если запрос не пустой
                    formula_latex[i][j] = rows_lat[0][0] # заменяем аббревиатуру на латинское название
                else:
                    formula_latex[i][j] = '' # если не нашёл, то пустой 
            # оставляем только не пустые значения
            formula_latex[i] = [ind for ind in formula_latex[i] if ind!='']
                
        # все латинские имена
        row_all_lat = self.cursor.execute("SELECT Latin_name \
                                     FROM basic_name_indicator \
                                     ORDER BY idBasicName;;")
        row_all_lat = self.cursor.fetchall()
        
        all_latin_name = [] # массив с латинскими именами
        # добавление в массив всех элементов запроса
        for i in range(len(row_all_lat)):
            all_latin_name.append(row_all_lat[i][0])
            self.color_vs.append([0,0,1]) # цвет у вершин голубой
        n = len(all_latin_name) # количество покавсех показателей
        
        self.edges_graph = [] # массив с рёбрами (кортежы)
        for i in range(n): # для всех показателей
            for j in range(len(base_name)): # для показателей, которые имеют формулу
                if all_latin_name[i] == base_name[j]: # если совпадают
                    # формула не пустая (в БД есть показатели из формулы)
                    if (len(formula_latex[j]))!=0: 
                        for h in range(len(formula_latex[j])): # для каждого аргумента
                            # находим индекс показателя
                            m = all_latin_name.index(formula_latex[j][h]) 
                            self.edges_graph.append((i,m)) # добавляем ребро
        
        self.vertices_label += all_latin_name # добавляем в подписи к вершинам
        
        ##### ПОКАЗАТЕЛИ, ФОРМИРУЕМЫЕ ПО МЕТОДИКЕ--------------------------------------
        # запрос, которые выводит всю таблицу formed_idicator_method, но
        # вместо id показатели и методики выводит латинское название показателя
        # и название методики на русском языке
        row_meth_ind = self.cursor.execute("SELECT Latin_name, Name_method_Russian \
                                      FROM (formed_idicator_method LEFT JOIN basic_name_indicator \
                                      ON formed_idicator_method.idBasicName = basic_name_indicator.idBasicName) \
                                      LEFT JOIN method ON formed_idicator_method.idMethod = method.idMethod \
                                      ORDER BY formed_idicator_method.idFormed_indicator;")
        row_meth_ind = self.cursor.fetchall()
        
        formed_ind = [] # создание массива с показателями
        formed_meth = [] # создание массива с методиками
        for i in range(len(row_meth_ind)): # проходимя по строкам запроса
            formed_ind.append(row_meth_ind[i][0])
            if row_meth_ind[i][1] == None: # если ещё не добавлена методика у показателя
                formed_meth.append('') # пустой
            else: # иначе
                formed_meth.append(row_meth_ind[i][1])  # добавляем
                
        # добавляем уникальные (не повторяющиеся) названия методик
        self.vertices_label += list(set(formed_meth)) 
        empty = ''
        # удаляем пустые значения (если есть)
        while empty in self.vertices_label: self.vertices_label.remove(empty) 
        
        for i in range(n): # проходимся по всем показателям (см.ранее)
            for j in range(len(formed_ind)): # показатели, которые сформерованы по методике
                if self.vertices_label[i] == formed_ind[j]: # совпадают
                    met = formed_meth[j] # ищем соответвующую методику
                    if met != '': # если не пустая
                        # добавялем ребро
                        self.edges_graph.append((i,self.vertices_label.index(met)))
        
        #### МЕТОДИКИ И ОБОРУДОВАНИЕ, НА КОТОРОМ ОНИ ИЗМЕРЯЮТСЯ------------------------  
        # запрос таблицы unit_method_equip, но выводятся русское название методики
        # и название оборудования
        rows_met_eq = self.cursor.execute("SELECT Name_method_Russian, Name_equipment \
                                     FROM (unit_method_equip INNER JOIN method \
                                     ON unit_method_equip.idMethod = method.idMethod) \
                                     INNER JOIN equipment ON unit_method_equip.idEquipment = equipment.idEquipment;")
        rows_met_eq = self.cursor.fetchall()
        
        met = [] # создание массива с методиками
        eq = [] # создание массива с оборудованием
        for i in range(len(rows_met_eq)): # заполнение данных по запросу
            met.append(rows_met_eq[i][0]) # методика
            eq.append(rows_met_eq[i][1]) # оборудование
        
        # добавление методик, которые ещё не связаны с показателями
        for i in range(n,len(self.vertices_label)): # не влючая сами показатели!
            self.color_vs.append([0,1,0]) # цвет методик зелёный
            for j in range(len(met)): 
                if self.vertices_label[i]!=met[j]: # если ещё такой не было
                    self.vertices_label.append(met[j]) # добавляем
                    self.color_vs.append([0,1,0]) # зелёный
        
        self.vertices_label += list(set(eq)) # названия оборудования в список с вершинами
        
        for i in range(len(list(set(eq)))): # цвет для вершин с оборудованием
            self.color_vs.append([1,1,0]) # жёлтый
        for i in range(n,len(self.vertices_label)): # проходимся по массиву не влючая показатели!
            for j in range(len(met)):
                if self.vertices_label[i]==met[j]: # соответствуют
                    e = eq[j] # оборудование
                    self.edges_graph.append((i,self.vertices_label.index(e))) # добавляем ребро
        
        ##### ПОКАЗАТЕЛИ И СИСТЕМЫ ОРГАНИЗМА, К КОТОРЫМ ОТНОСЯТСЯ----------------------
        # Запрос для вывода латинским имён показателей и названия системы
        row_ind_sys = self.cursor.execute("SELECT Latin_name, Name_systems \
                                     FROM basic_name_indicator INNER JOIN systems_indicator \
                                     ON basic_name_indicator.idGroupSystems = systems_indicator.idGroupSystems;")
        row_ind_sys = self.cursor.fetchall()
        
        indic = [] # создаём массив с показателями
        systems = [] # создаём массив с системами
        # заполняем массивы по запросу
        for i in range(len(row_ind_sys)):
            indic.append(row_ind_sys[i][0])
            systems.append(row_ind_sys[i][1])
            
        self.vertices_label += list(set(systems)) # добавляем названия 
        for i in range(n): # проходимся по показателям
            for j in range(len(indic)): # по показателям из запроса
                if self.vertices_label[i]==indic[j]: # совпадают
                    sys = systems[j] # находим соотвествующую системы
                    self.color_vs.append([1,0,0]) # задаём цвет - красный
                    self.edges_graph.append((i,self.vertices_label.index(sys))) # добавляем ребро
        self.origin_vs = self.vertices_label.copy()
        
        ### ОТОБРАЖЕНИЕ В ВИДЕ НАПРАВЕЛЕННОГО ГРАФА
        #####-----------------
        # редактирование подписей к вершинам по разделителю
        '''
        for i in range(len(self.vertices_label)):
            text_label = self.vertices_label[i]
            self.vertices_label[i] = text_label.replace(" ", "\n") # расзделитель пробел
        for i in range(len(self.vertices_label)):
            text_label = self.vertices_label[i]
            self.vertices_label[i] = text_label.replace("-", "\n") # разделитель дефис 
        self.g = igraph.Graph(directed = True) # напревленный граф
        self.g.add_vertices(len(self.vertices_label)) # количество вершин
        #self.g.vs["label"] = self.vertices_label # подписи вершин
        self.g.vs['color'] = self.color_vs # цвета вершин
        self.g.vs["size"] = 60 # размер вершин
        self.g.vs["label_size"] = 10 # размер подписи
        self.g.add_edges(edges_graph) # добавление рёбер
        self.g.es["width"] = 1.2 # ширина ребра
        self.layout = self.g.layout_reingold_tilford_circular() # стиль графа в общем
        # построение графа
        igraph.plot(self.g, "test_indic.png", layout = self.layout,bbox = (800,800),margin = (35,80,35,80))
        '''
    def saveas_file(self): #сохранить изображение как (смена имени или выбор другой папки)
        #выбор папки и имени для сохранения
        self.name = QFileDialog.getSaveFileName(self, 'Сохранить как','', "*.png")[0]
        self.image = ImageQt.fromqimage(self.img.pixmap())
        self.image.save(self.name) #сохранить под новым именем
        QMessageBox.information(self, 'Сообщение', "Ваше изображение сохранено")
        
    def big(self): #увеличение изображения
        w = self.image.size[0] #ширина изображения
        h = self.image.size[1] #высота изображения
        val=self.ScrollBar_big.value() #значение процента для увеличения (от 100 до 500)
        x = round((val/100)*w) #новое значение ширины
        y = round((val/100)*h) #новое значение высоты
        self.photo = QPixmap(ImageQt.toqpixmap(self.image.resize((x, y)))) #изображение pixmap
        self.img.setPixmap(self.photo) #добавляем на виджет
        
    def small(self): #уменьшение изображения
        w = self.image.size[0] #ширина изображения
        h = self.image.size[1] #высота изображения
        val=self.ScrollBar_small.value() #значение процента для уменьшения (от 100 до 500)
        x = round(w/(val/100)) #новое значение ширина
        y = round(h/(val/100)) #новое значение высоты
        self.photo = QPixmap(ImageQt.toqpixmap(self.image.resize((x, y)))) #изображение pixmap
        self.img.setPixmap(self.photo)  #добавляем на виджет
        
    def update_graph(self):
        check = self.checkBox_abbrev.isChecked()
        self.g = igraph.Graph(directed = True)
        self.g.add_vertices(len(self.vertices_label)) # количество вершин
        self.lang = self.language_indicator.currentText()
        
        if self.lang != "Латинские названия":
            self.lat = []
            self.lang_name = []
            err = 0
            err1 = 0
            #if self.rows_lang == ():
                #QMessageBox.information(self, 'Предупреждение',
                                        #"К сожалению, дополнительных названий на данном языке нет. Но вы можете видеть только названия на латыни")
                #self.language_indicator.setCurrentIndex(0)
                #self.vertices_label = self.origin_vs.copy()
            #else:
            self.new_vertices_label = self.origin_vs.copy()
            for i in range(len(self.new_vertices_label)):
                row_lang = self.cursor.execute("SELECT Decoding_abbrev \
                                FROM (additional_name INNER JOIN basic_name_indicator \
                                ON additional_name.idBasicName = basic_name_indicator.idBasicName) \
                                INNER JOIN language_add_indicator \
                                ON additional_name.idLanguage = language_add_indicator.idLanguage \
                                WHERE (Name_language='%s') AND (Latin_name='%s')\
                                ORDER BY idAddName limit 1;" \
                                %(self.lang, self.new_vertices_label[i]))
                row_lang = self.cursor.fetchall()
                #print(row_lang)
                if row_lang == ():
                    err += 1
                else:
                    self.new_vertices_label[i] = row_lang[0][0]
            if err == len(self.new_vertices_label):
                QMessageBox.information(self, 'Предупреждение',
                                        "К сожалению, дополнительных названий на данном языке нет. Но вы можете видеть только названия на латыни")
                self.language_indicator.setCurrentIndex(0)
                self.vertices_label = self.origin_vs.copy()
                err = 0
            else:
                if check==False:
                    self.vertices_label = self.new_vertices_label
                else:
                    self.new_vertices_label_1 = self.new_vertices_label.copy()
                    for i in range(len(self.new_vertices_label_1)):
                        row_abb = self.cursor.execute("SELECT Abbreviation_add_name \
                                                      FROM additional_name \
                                                      WHERE (Decoding_abbrev='%s')\
                                                      ORDER BY idAddName;" \
                                                      % self.new_vertices_label_1[i])
                        row_abb = self.cursor.fetchall()
                        if row_abb == ():
                            err1 += 1
                        else:
                            self.new_vertices_label_1[i] = row_abb[0][0]
                    
                    if err1 == len(self.new_vertices_label_1):
                        QMessageBox.information(self, 'Предупреждение',
                                        "Для данного языка нет аббревиатур")
                        self.vertices_label = self.new_vertices_label
                        err1 = 0
                    else:
                        #print(self.new_vertices_label_2)
                        self.new_vertices_label_2 = self.new_vertices_label_1.copy()
                        row_sh_lt_add = self.cursor.execute("SELECT Latin_name, Short_name \
                                                FROM basic_name_indicator;")
                        row_sh_lt_add = self.cursor.fetchall()
                        lat_add = []
                        sh_add = []
                        for i in range(len(row_sh_lt_add)):
                            lat_add.append(row_sh_lt_add[i][0])
                            sh_add.append(row_sh_lt_add[i][1])
                        #print(lat_add)
                        #print(sh_add)
                        #print(self.new_vertices_label_2)
                        for i in range(len(self.new_vertices_label_2)):
                            for j in range(len(lat_add)):
                                if self.new_vertices_label_2[i]==lat_add[j]:
                                    #print("ОК")
                                    self.new_vertices_label_2[i] = sh_add[j]
                                    #print(self.new_vertices_label_2[i])
                        #print(self.new_vertices_label_2)
                        
                        self.vertices_label = self.new_vertices_label_2
        else:
            if check==False:
                self.vertices_label = self.origin_vs.copy()
            else:
                self.ver_short_latin = self.origin_vs.copy()
                row_sh_lt = self.cursor.execute("SELECT Latin_name, Short_name \
                                                FROM basic_name_indicator;")
                row_sh_lt = self.cursor.fetchall()
                lat = []
                sh = []
                for i in range(len(row_sh_lt)):
                    lat.append(row_sh_lt[i][0])
                    sh.append(row_sh_lt[i][1])
                for i in range(len(self.ver_short_latin)):
                    for j in range(len(lat)):
                        if self.ver_short_latin[i] == lat[j]:
                            self.ver_short_latin[i] = sh[j]
                self.vertices_label = self.ver_short_latin    
            
            
        self.output_vs = self.vertices_label.copy()
        for i in range(len(self.output_vs)):
            text_label = self.output_vs[i]
            self.output_vs[i] = text_label.replace(" ", "\n") # расзделитель пробел
        for i in range(len(self.output_vs)):
            text_label = self.output_vs[i]
            self.output_vs[i] = text_label.replace("-", "\n") # разделитель дефис
        self.g.vs["label"] = self.output_vs
        self.g.vs['color'] = self.color_vs # цвета вершин
        self.g.vs["size"] = 60 # размер вершин
        self.g.vs["label_size"] = 10 # размер подписи
        self.g.add_edges(self.edges_graph) # добавление рёбер
        self.g.es["width"] = 1.2 # ширина ребра
        self.layout = self.g.layout_reingold_tilford_circular() # стиль графа в общем
        # построение графа
        igraph.plot(self.g, "test_indic.png", layout = self.layout,bbox = (800,800),margin = (35,80,35,80))
        # запрос
        self.filename = os.path.abspath("test_indic.png")
        self.image = Image.open(self.filename) #открыть файл как изображение
        self.photo = QPixmap(ImageQt.toqpixmap(self.image))
        self.img.setPixmap(self.photo) #вывести изображение
        


#вызов окна 
if __name__ == '__main__': 
   app = QApplication(sys.argv) 
   form = Main() 
   form.show() 
   app.exec() 