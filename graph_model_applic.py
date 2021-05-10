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
import math

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

    def big(self): #увеличение изображения
        w = self.image.size[0] #ширина изображения
        h = self.image.size[1] #высота изображения
        val=self.ScrollBar_big.value() #значение процента для увеличения (от 100 до 500)
        x = round((val/100)*w) #новое значение ширины
        y = round((val/100)*h) #новое значение высоты
        self.photo = QPixmap(ImageQt.toqpixmap(self.image.resize((x, y)))) #изображение pixmap
        #self.width.setText(str(x)+' px') #вывод ширины
        #self.height.setText(str(y)+' px') #вывод высоты
        self.img.setPixmap(self.photo) #добавляем на виджет
        
    def small(self): #уменьшение изображения
        w = self.image.size[0] #ширина изображения
        h = self.image.size[1] #высота изображения
        val=self.ScrollBar_small.value() #значение процента для уменьшения (от 100 до 500)
        x = round(w/(val/100)) #новое значение ширина
        y = round(h/(val/100)) #новое значение высоты
        self.photo = QPixmap(ImageQt.toqpixmap(self.image.resize((x, y)))) #изображение pixmap
        #self.width.setText(str(x)+' px') #вывод ширины
        #self.height.setText(str(y)+' px') #вывод высоты
        self.img.setPixmap(self.photo)  #добавляем на виджет

    def update_graph(self):
        # запрос
        print(self.language_indicator.currentText()) # язык из выпадающего списка 
        #webbrowser.open_new_tab("test1.png") #открытие созданного файла
        filename = os.path.abspath("test_indic.png")
        self.image = Image.open(filename) #открыть файл как изображение
        self.photo = QPixmap(ImageQt.toqpixmap(self.image))
        self.img.setPixmap(self.photo) #вывести изображение
        
#вызов окна 
if __name__ == '__main__': 
   app = QApplication(sys.argv) 
   form = Main() 
   form.show() 
   app.exec() 