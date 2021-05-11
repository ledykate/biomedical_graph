# -*- coding: utf-8 -*-
"""
Created on Thu May  6 13:25:05 2021

@author: Катрина
"""

import MySQLdb # библиотека для работы с MySQL
import numpy as np # работа с массивами
import igraph # библиотека для работы с графами
#import webbrowser # для открытия файла с построенным графом
import sys
import os
from parse_latex import parse_latex
from my_graph import my_graph

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
              
        self.vertices_label, self.color_vs, self.edges_graph = my_graph(self.cursor)
        self.origin_vs = self.vertices_label.copy()
        
        ### ОТОБРАЖЕНИЕ В ВИДЕ НАПРАВЕЛЕННОГО ГРАФА
        #####-----------------
        # редактирование подписей к вершинам по разделителю

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
                        err1 = 0
                        self.new_vertices_label_3 = self.new_vertices_label.copy()
                        row_sh_lt_add = self.cursor.execute("SELECT Latin_name, Short_name \
                                                FROM basic_name_indicator;")
                        row_sh_lt_add = self.cursor.fetchall()
                        lat_add_ = []
                        sh_add_ = []
                        for i in range(len(row_sh_lt_add)):
                            lat_add_.append(row_sh_lt_add[i][0])
                            sh_add_.append(row_sh_lt_add[i][1])
                        for i in range(len(self.new_vertices_label_3)):
                            for j in range(len(lat_add_)):
                                if self.new_vertices_label_3[i]==lat_add_[j]:
                                    self.new_vertices_label_3[i] = sh_add_[j]
                        self.vertices_label = self.new_vertices_label_3
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