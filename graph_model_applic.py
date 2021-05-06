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
        self.conn = MySQLdb.connect('localhost', 'root', 'root','mydb',charset='utf8', 
                       use_unicode = True)
        self.cursor = self.conn.cursor()
        
        self.pushButton_update.clicked.connect(self.update_graph)
        #self.setWindowIcon(QIcon('icon.png'))
        #передвигать изображение
        lay = QVBoxLayout(self.scrollAreaWidgetContents)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.img)
        self.imageScrollArea.setWidgetResizable(True)
        self.img.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        
        self.image = None #изображение (pillow)
        self.photo = None #изображение в виджите (pixmap)
        
    def update_graph(self):
        # запрос
        rows=self.cursor.execute("SELECT group_prt.Title_grp, type_prt.Name_TP \
                            FROM type_prt INNER JOIN group_prt ON type_prt.idType_Prt = group_prt.idType_Prt \
                            WHERE (((type_prt.idType_Prt)=1));")
        rows = self.cursor.fetchall() # получение данных из запроса
        # двумерный массив с результатом запроса в качестве строк массива
        fiz_sistem = [[0 for i in range(len(rows[0]))] for j in range(len(rows))]
        #Получаем данные
        for i in range(len(rows)):
            fiz_sistem[i][0] = rows[i][0] # Title_grp
            fiz_sistem[i][1] = rows[i][1] # Name_TP
        # преобразование в тип numpy для дальнейшего удобства
        fiz_sistem = np.array(fiz_sistem) 
        # уникальные значения из первого столбца
        unq_group = np.unique(fiz_sistem[:,0],axis = 0) 
        # уникальные значения из второго столбца
        unq_types = np.unique(fiz_sistem[:,1],axis = 0)
        # количество уникальных элементов
        n = unq_group.shape[0] + unq_types.shape[0]
        # формирование матрицы смежности
        matrix_smeg = [[0 for i in range(n)]for j in range(n)]
        # массив с рёбрами графа
        edges_graph = []
        # формируем матрицу смежности только для первого столбца
        for i in range(n):
            for j in range(n):
                if i!=0 and j==0:
                    matrix_smeg[i][j] = 1 # вес ребра (или если 1 - просто есть)
                    edges_graph.append((i,j)) # добавляем пару входа и выхода ребра
        # подписи к вершинам
        label_graph = (np.concatenate([unq_types,unq_group]).T).tolist()
        # для лучшего отображения поменяем пробел на перенос строки
        for i in range(len(label_graph)):
            text_label = label_graph[i]
            label_graph[i] = text_label.replace(" ", "\n")
        ### ОТОБРАЖЕНИЕ В ВИДЕ НАПРАВЕЛЕННОГО ГРАФА
        #####-----------------
        g = igraph.Graph(directed = True) # напревленный граф
        g.add_vertices(len(label_graph)) # количество вершин
        g.vs["label"] =  label_graph # подписи вершин
        g.add_edges(edges_graph) # рёбра
        g.es['color'] = ['green', 'red', 'blue', 'yellow','black'] # цвета рёбер
        # построение графа
        igraph.plot(g, "test1.png", bbox = (800,800),
                    vertex_label_size = 12, vertex_size = 80, margin = (100,45,100,45),
                    # цвета вершин
                    vertex_color = ['red','green','green','green','green','green'])  
        #webbrowser.open_new_tab("test1.png") #открытие созданного файла
        filename = os.path.abspath("test1.png")
        self.image = Image.open(filename) #открыть файл как изображение
        self.photo = QPixmap(ImageQt.toqpixmap(self.image))
        self.img.setPixmap(self.photo) #вывести изображение
        
#вызов окна 
if __name__ == '__main__': 
   app = QApplication(sys.argv) 
   form = Main() 
   form.show() 
   app.exec() 