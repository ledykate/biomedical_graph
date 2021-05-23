import  # запуск окна
import os # поиск файла
import MySQLdb # библиотека для работы с MySQL
import igraph # библиотека для работы с графами
import numpy as np # формирование случайно последовательности
from my_graph import my_indicator, my_graph, syst_ind # функция для построения графа

from PIL import Image, ImageQt # библиотека по работе с изображениями PIL (pillow)
## Работа с библиотекой PyQt5 для работы интерфейса
from PyQt5.QtWidgets import QMainWindow, QFileDialog,QApplication, QMessageBox,QVBoxLayout
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.Qt import QHeaderView

class Main(QMainWindow): # класс, где храняться все действия
    def __init__(self): # служебная функция инициализации,загрузка окна
        QMainWindow.__init__(self)
        loadUi("biomedical_interface.ui",self) # файл с расположение с дизайном
        self.setWindowTitle('Графовые модели') # заголовок приложение
        # подключение к базе данных biomedical_indicators
        self.conn = MySQLdb.connect('localhost', 'root', 'root',
                                    'biomedical_indicators',
                                    charset = 'utf8', 
                                    use_unicode = True)
        self.cursor = self.conn.cursor()
        self.setWindowIcon(QIcon('icon.png')) # иконка приложения
        
        # ползунок для просмотра изображения
        lay = QVBoxLayout(self.scrollAreaWidgetContents)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.img)
        self.imageScrollArea.setWidgetResizable(True)
        self.img.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        # переменные для работы с изображением графа
        self.image = None #изображение (pillow)
        self.photo = None #изображение в виджите (pixmap)
        
        global click_update # глобальная переменная
        click_update = 0 # переменная отвечающая за корректное нажатие кнопки и данных
        
        self.pushButton_update.clicked.connect(self.update_ind) # кнопка обновления данных
        self.checkBox_all_ind.stateChanged.connect(self.change_all) # выбор всех показателей
        self.pushButton_plot_graph.clicked.connect(self.plot_graph) # кнопка построения графа
        self.ScrollBar_big.valueChanged.connect(self.big) #увелечение изображения 
        self.ScrollBar_small.valueChanged.connect(self.small) #уменьшение изображения
        self.saveas_graph.triggered.connect(self.saveas_file) #сохранить/сохранить как
        self.equipment_ind.currentTextChanged.connect(self.activated_equip)  # вывод показателей по оборудованию
        
        # задание значений для выпадающего списка
        # запрос из БД
        rows = self.cursor.execute("SELECT Name_language \
                                   FROM language_add_indicator;")
        rows = self.cursor.fetchall() # получение данных из запроса
        L = []
        # заполнение массива
        for i in range(len(rows)):
            L.append(rows[i][0])
        L.insert(0,'Латинские названия')
        self.language_indicator.addItems(L) # добавление значений в выпадающий список
                         
        # Флажки для выбора система организма
        self.row_sys = self.cursor.execute("SELECT Name_systems\
                                           FROM basic_name_indicator \
                                           INNER JOIN systems \
                                           ON basic_name_indicator.idSystem = systems.idSystem \
                                           GROUP BY Name_systems \
                                           ORDER BY systems.idSystem;")
        self.row_sys = self.cursor.fetchall()
        self.sys_ind = []
        for i in range(len(self.row_sys)):
            self.sys_ind.append(self.row_sys[i][0]) # добавление значений в массив
            
        # задание цветов по системе
        self.color_orig = []
        for j in range(len(self.row_sys)):
            col = np.random.sample(3) # рандомное значение от 0 до 1 (палитра RGB)
            self.color_orig.append(col.tolist()) # преобразование в список
            
        # создание флажков в таблице с системами
        self.table_systems.setRowCount(len(self.sys_ind)) # изменяем количество строк
        self.table_systems.setColumnCount(1)  # изменяем количество столбцов  
        self.table_systems.setHorizontalHeaderLabels(["Система организма"]) # заголовок столбца
        for i in range(len(self.sys_ind)):
            item = QtWidgets.QTableWidgetItem() # создаём ячейку
            self.table_systems.setItem(i, 0, item) # обновляем ячейку
            check_box = QtWidgets.QCheckBox(self.sys_ind[i]) # создаём флажок
            item.setFlags(QtCore.Qt.ItemIsEnabled) # запрещаем редактировать
            self.table_systems.setCellWidget(i, 0, check_box) # добавлем флажок в ячейку
            # задание цвета ячейке
            self.table_systems.item(i, 0).setBackground(QColor(self.color_orig[i][0]*255,
                                   self.color_orig[i][1]*255, self.color_orig[i][2]*255))
        self.table_systems.horizontalHeader().setStretchLastSection(True) # растянуть последний столбец
        
    ## ИЗМЕНЕНИЕ РАЗМЕРА ИЗОБРАЖЕНИЕ
    def big(self): #увеличение изображения
        w = self.image.size[0] #ширина изображения
        h = self.image.size[1] #высота изображения
        val = self.ScrollBar_big.value() #значение процента для увеличения (от 100 до 500)
        x = round((val / 100) * w) #новое значение ширины
        y = round((val / 100) * h) #новое значение высоты
        self.photo = QPixmap(ImageQt.toqpixmap(self.image.resize((x, y)))) #изображение pixmap
        self.img.setPixmap(self.photo) #добавляем на виджет
    
    def small(self): #уменьшение изображения
        w = self.image.size[0] #ширина изображения
        h = self.image.size[1] #высота изображения
        val = self.ScrollBar_small.value() #значение процента для уменьшения (от 100 до 500)
        x = round(w / (val / 100)) #новое значение ширина
        y = round(h / (val / 100)) #новое значение высоты
        self.photo = QPixmap(ImageQt.toqpixmap(self.image.resize((x, y)))) #изображение pixmap
        self.img.setPixmap(self.photo)  #добавляем на виджет
     
    ## КНОПКА ОБНОВЛЕНИЯ
    def update_ind(self):
        global click_update # глобальная
        # соеденение с базой
        self.conn = MySQLdb.connect('localhost', 'root', 'root',
                                    'biomedical_indicators',
                                    charset = 'utf8', 
                                    use_unicode = True)
        self.cursor = self.conn.cursor()
        # положение ползунков масштаба после обновления
        self.ScrollBar_small.setValue(100)
        self.ScrollBar_big.setValue(100)
        self.equipment_ind.clear() # очистка списка с оборудованием
        self.sys_check = [] # выбранные флажки систем
        # считываение какие флажки системы выбраны 
        for i in range(len(self.sys_ind)):
            k = (self.table_systems.cellWidget(i, 0)).isChecked() # состояние флажка
            if k == True: # если выбран
                self.sys_check.append(i+1) # добавляем в массив
        if len(self.sys_check) != 0: # если выбраны флажки
            click_update = 1
            # данные, которые получены из функции my_graph:
            # количество показателей, подписи вершин
            self.n, self.vertices_label = my_indicator(self.sys_check,self.cursor)
            self.origin_vs = self.vertices_label.copy() # копия исходнных данных

            self.check = self.checkBox_abbrev.isChecked() # значение флажка включения аббревиатуры
            self.lang = self.language_indicator.currentText() # значение языка из выпадающего списка
        
            self.m = 0 # переменная количества столбцов в таблице (с и без аббревиатуры)
            if self.lang != "Латинские названия": # Доп. имена на разных языках
                err = 0 # переменная для ошибки
                # копия списка вершин (нужна для динамического обновления)
                self.new_vertices_label = self.origin_vs.copy()
                # находим первое доплнительное имя на заданном языке для 
                # определённого базового показателя
                for i in range(len(self.new_vertices_label)): 
                    row_lang = self.cursor.execute("SELECT Decoding_abbrev \
                                    FROM (additional_name INNER JOIN basic_name_indicator \
                                    ON additional_name.idBasicName = basic_name_indicator.idBasicName) \
                                    INNER JOIN language_add_indicator \
                                    ON additional_name.idLanguage = language_add_indicator.idLanguage \
                                    WHERE (Name_language = '%s') AND (Latin_name = '%s')\
                                    ORDER BY idAddName limit 1;" \
                                    %(self.lang, self.new_vertices_label[i])) # язык, баз.показателья
                    row_lang = self.cursor.fetchall() # получаем данные
                    if row_lang == (): # если запрос пустой
                        err += 1 # ошибка
                    else: # иначе
                        self.new_vertices_label[i] = row_lang[0][0] # изменяем значение 
                        
                if err == len(self.new_vertices_label): # если все ошибки
                    # доп. имён такого показателя ещё нет
                    QMessageBox.information(self, 'Предупреждение',
                                            "К сожалению, дополнительных названий на данном языке нет. Но вы можете видеть только названия на латыни")
                    # переключаем язык для вывода базовых имён показателей
                    self.language_indicator.setCurrentIndex(0) 
                    # список имён вершин - исходный
                    self.vertices_label = self.origin_vs.copy()
                    err = 0 # обнуляем ошибки
                    self.m = 1 # вывод только баз.имён показателей
                    self.checkBox_abbrev.setChecked(False) # флажок не влючён
                    
                else: # ошибок нет, то
                    if self.check == False: # флажок выключен
                        # найденный имена по запросу выводятся на графе 
                        # как название вершины
                        self.vertices_label = self.new_vertices_label 
                        self.m = 2 # выводим баз.имя и доп.имя на заданном языке
                    else: # флажок включён
                        self.m = 3 # для вывода баз.имени, доп.имени и аббревиатуры
                        # создаём копию ранее найденных имён
                        self.new_vertices_label_sh = self.new_vertices_label.copy()
                        # находим аббревиатуру для этого имени
                        for i in range(len(self.new_vertices_label_sh)):
                            row_abb = self.cursor.execute("SELECT Abbreviation_add_name \
                                                          FROM additional_name \
                                                          WHERE Decoding_abbrev = '%s'" \
                                                          % self.new_vertices_label_sh[i])
                            row_abb = self.cursor.fetchall()
                            if row_abb != (): # если не пустая, перезаписываем
                                self.new_vertices_label_sh[i] = row_abb[0][0]
                        self.vertices_label = self.new_vertices_label_sh   
                        
            else: # вывод базовых имён показателей
                if self.check == False: # флажок выключен
                    self.m = 1 # выводим только баз.имена
                    self.vertices_label = self.origin_vs.copy() # имена вершин
                else: # флажок включен
                    self.m = 2 # выводим баз.имя и аббревиатуру
                    # копия для динамического обновления
                    self.ver_short_latin = self.origin_vs.copy()
                    # запрос для аббревиатуры
                    for i in range(len(self.ver_short_latin)):
                        row_sh_lt = self.cursor.execute("SELECT Short_name \
                                                        FROM basic_name_indicator \
                                                        WHERE Latin_name = '%s'" \
                                                        % self.ver_short_latin[i])
                        row_sh_lt = self.cursor.fetchall()
                        if row_sh_lt != (): # запрос не пустой
                            self.ver_short_latin[i] = row_sh_lt[0][0] # изменяем
                    self.vertices_label = self.ver_short_latin # имена вершин
            # поиск оборудования в зависимости от системы организма
            row_eq = self.cursor.execute("SELECT Name_equipment \
                                         FROM basic_name_indicator \
                                         INNER JOIN (((unit_method_equip \
                                         INNER JOIN method \
                                         ON unit_method_equip.idMethod = method.idMethod) \
                                         INNER JOIN equipment \
                                         ON unit_method_equip.idEquipment = equipment.idEquipment) \
                                         INNER JOIN formed_idicator_method \
                                         ON method.idMethod = formed_idicator_method.idMethod) \
                                         ON basic_name_indicator.idBasicName = formed_idicator_method.idBasicName \
                                         GROUP BY idSystem, Name_equipment \
                                         HAVING idSystem IN %s" \
                                         % syst_ind(self.sys_check))
            row_eq = self.cursor.fetchall()
            self.equip = [] # массив с оборудованием
            for i in range(len(row_eq)):
                self.equip.append(row_eq[i][0]) # добавляем в массив
            if len(self.equip) != 0: # если не пустой
                self.equipment_ind.addItems(self.equip) # добавляем в выдающий список
            else:
                # иначе выводим сообщение
                QMessageBox.information(self, 'Сообщение', "У показателей данных(ой) систем(ы) неизвестно оборудованиe для измерения")
                self.equipment_ind.clear() # очисщаем список
                # очищаем таблицу
                self.table_equip_ind.setRowCount(0)
                self.table_equip_ind.setColumnCount(0)

            ## ЗАПОЛНЕНИЕ ТАБЛИЦЫ ДАННЫММИ  
            if self.m>0: # ненулевое количество столбцов
                self.table_ind.setRowCount(self.n) # изменяем количество строк
                self.table_ind.setColumnCount(self.m+1)  # изменяем количество столбцов
                text = ["Выбрать", "Показатель","Расшифровка","Аббревиатура"] # подписи столцов
                for i in range(self.n):
                    # вставка флажков в таблицу для выбора показателя
                    item_fl = QtWidgets.QTableWidgetItem() # создаём ячейку
                    check_box_fl = QtWidgets.QCheckBox() # создаём флажок
                    # центрируем флажок
                    check_box_fl.setStyleSheet("margin-left:50%; margin-right:50%;")
                    item_fl.setFlags(QtCore.Qt.ItemIsEnabled) # запрещаем редактировать
                    self.table_ind.setCellWidget(i, 0, check_box_fl) # добавлем флажок в ячейку
                                       
                    name1 = self.origin_vs[i] # базовое имя показателя
                    new_item_1 = QtWidgets.QTableWidgetItem(name1) # ячейка
                    new_item_1.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать   
                    self.table_ind.setItem(i, 1, new_item_1) # добавляем в первый столбец
                    
                    row_color_ind = self.cursor.execute("SELECT idSystem \
                                         FROM basic_name_indicator \
                                         WHERE Latin_name = '%s'" \
                                         % name1)
                    row_color_ind = self.cursor.fetchall()
                    color_ind = row_color_ind[0][0]
                    self.table_ind.item(i, 1).setBackground(QColor(self.color_orig[color_ind-1][0]*255, 
                                       self.color_orig[color_ind-1][1]*255,self.color_orig[color_ind-1][2]*255))
                    
                    if self.m >= 2: # для вывод доп.имён
                        if self.lang=="Латинские названия": # если базовые имена
                            # флафок влючён - вывод аббревиатур 
                            name2 = self.ver_short_latin[i] 
                        else: # доп.имена
                            # флажок выключен 
                            name2 = self.new_vertices_label[i] # доп.имя
                            if name1 == name2: # если есть совпадения
                                name2 = "" # делаем ячейку пустой
                        new_item_2 = QtWidgets.QTableWidgetItem(name2) # ячейка
                        new_item_2.setFlags(QtCore.Qt.ItemIsEnabled) # запрещаем редактировать 
                        # добавляем во второй столбец
                        self.table_ind.setItem(i, 2, new_item_2)  
                        # аббревиатуры языка
                        if self.lang != "Латинские названия" and self.m == 3: 
                            name3 = self.new_vertices_label_sh[i] # находим аббревиатуру
                            if name1 == name3: # совпадющие
                                name3 = "" # пустые
                            new_item_3 = QtWidgets.QTableWidgetItem(name3) # ячейка
                            new_item_3.setFlags(QtCore.Qt.ItemIsEnabled) #запрещаем редактировать 
                            # добавлем в 3 столбцец
                            self.table_ind.setItem(i, 3, new_item_3)
                # растягивание последнего столбца  
                #self.table_ind.horizontalHeader().setStretchLastSection(True)
                # автоматические подбор ширины столбца
                self.table_ind.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.table_ind.horizontalHeader().setMinimumSectionSize(0)
                # подписи к столбца для заданного количества
                if self.m == 1:
                    self.table_ind.setHorizontalHeaderLabels(text[:2])
                elif self.m == 2:
                    self.table_ind.setHorizontalHeaderLabels(text[:3])
                elif self.m == 3:
                    self.table_ind.setHorizontalHeaderLabels(text[:])
            else: # если количество столбцов равно m = 0
                self.table_ind.setRowCount(0)
            #click_update = 0
        else: # не выбран ни одни флажок
            click_update = 0
            # сообщение
            QMessageBox.information(self, 'Предупреждение',
                                            "Вы не выбрали системы организма!")
            #self.language_indicator.setCurrentIndex(0) # язык латинский
            self.checkBox_abbrev.setChecked(False) # флажок не влючён
            self.ScrollBar_small.setValue(100)
            self.ScrollBar_big.setValue(100)
            self.table_ind.setRowCount(0)
            self.table_ind.setColumnCount(0)
            self.table_equip_ind.setRowCount(0)
            self.table_equip_ind.setColumnCount(0)
            self.filename = ''
            self.photo = QPixmap() #очистка изображение pixmap
            self.img.setPixmap(self.photo) 
            self.equipment_ind.clear()
        #print(click_update)
        
    # ПОСТРОЕНИЕ ГРАФА    
    def plot_graph(self):
        global click_update
        if click_update == 1: # если данные обновлены
            is_check_ind = [] # индексы выбранных показателей
            latin_name_ch = [] # базовые имена выбранных показателей
            for i in range(self.n):
                k = (self.table_ind.cellWidget(i, 0)).isChecked() # состояние флажка
                if k == 1: # если выбран
                    is_check_ind.append(i) # добавляем инднкс
                    latin_name_ch.append(self.table_ind.item(i, 1).text()) # добавляем базовое имя
            if len(latin_name_ch) == 0: # не выбран ни один флажок
                QMessageBox.information(self, 'Сообщение', "Вы не выбрали ни одного показателя.\nВеберете хотя бы один")
                self.filename = ''
                self.photo = QPixmap()  # очистка изображение pixmap
                self.img.setPixmap(self.photo)
            else:
                # подключение к БД
                self.conn = MySQLdb.connect('localhost', 'root', 'root',
                                            'biomedical_indicators',charset = 'utf8',use_unicode = True)
                self.cursor = self.conn.cursor()
                # количество показателей, список вершин, цвет вершин, список рёбер
                n_ind, vertices_label_ind, color_vs, edges_graph = my_graph(latin_name_ch,self.cursor)
                # задание цвета для показателей
                for j in range(len(self.sys_check)):
                    for i in range(n_ind):
                        row_ind_sys = self.cursor.execute("SELECT idSystem \
                                         FROM basic_name_indicator \
                                         WHERE Latin_name = '%s'" \
                                         % vertices_label_ind[i])
                        row_ind_sys = self.cursor.fetchall()
                        if self.sys_check[j] == row_ind_sys[0][0]: # если показатель есть
                            color_vs[i] = self.color_orig[self.sys_check[j]-1] # задаём цвет
                # подписи к вершинам в соотвествии с фильтрами            
                vertices_label_graph = [0 for i in range(len(vertices_label_ind))]
                vertices_label_graph[n_ind:] = vertices_label_ind[n_ind:]
                if self.lang != "Латинские названия": # нелатинское название
                    if self.check == False: # без аббревиатуры
                        vertices_label_graph[:n_ind] = [self.new_vertices_label[i] for i in is_check_ind]
                    else: # с аббревиатурой
                        vertices_label_graph[:n_ind] = [self.new_vertices_label_sh[i] for i in is_check_ind] 
                else: # латинское название
                    if self.check == False: # без аббревиатуры
                        vertices_label_graph = vertices_label_ind.copy()
                    else: # с аббревиатурой
                        vertices_label_graph[:n_ind] = [self.ver_short_latin[i] for i in is_check_ind]
                
                ### ПОСТРОЕНИЕ графа
                self.g = igraph.Graph(directed = True) # создание направленного графа
                self.g.add_vertices(len(vertices_label_ind)) # количество вершин
                output_vs = vertices_label_graph.copy() # для вывода имён на графе
                # перенос имён по разделителю для удобного вывода
                for i in range(len(output_vs)):
                    text_label = output_vs[i]
                    output_vs[i] = text_label.replace(" ", "\n") # разделитель пробел
                for i in range(len(output_vs)):
                    text_label = output_vs[i]
                    output_vs[i] = text_label.replace("-", "\n") # разделитель дефис
                    
                self.g.vs["label"] = output_vs # подписи вершин
                self.g.vs["color"] = color_vs # цвета вершин
                self.g.vs["size"] = 70 # размер вершин
                self.g.vs["label_size"] = 10 # размер подписи
                self.g.add_edges(edges_graph) # добавление рёбер
                self.g.es["width"] = 1.2 # ширина ребра
                # нумерация рёбер
                self.g.es["weight"] = [i+1 for i in range(len(edges_graph))]
                self.g.es["label"] = self.g.es["weight"]
                
                # размер изображения
                b = int(self.spinBox_bbox_graph.value())
                bbox = (b,b)
                # стиль отображения графа
                self.layout = self.g.layout_fruchterman_reingold()
                
                # построение графа
                igraph.plot(self.g, "test_indic.png", layout = self.layout, 
                            bbox = bbox, margin = (50, 100, 50, 100))
                # вывод изображения с графом
                self.filename = os.path.abspath("test_indic.png")
                self.image = Image.open(self.filename) # открыть как изображение
                self.photo = QPixmap(ImageQt.toqpixmap(self.image))
                self.img.setPixmap(self.photo) #вывести изображение
        else:
            QMessageBox.information(self, 'Сообщение', "Вы не обновили данные")

    # выбор всех показателей
    def change_all(self, state):
        if click_update == 1: # если показтели выведены
            for i in range(self.n):
                if state == Qt.Checked: # выбран, то все флажки показателей выбраны
                    self.table_ind.cellWidget(i, 0).setChecked(True)
                else: # снят - сняты все флажки
                    self.table_ind.cellWidget(i, 0).setChecked(False)
        else:
            self.checkBox_all_ind.setChecked(False)
            QMessageBox.information(self, 'Сообщение', "Ещё не введены данные")
            
    # просмотр показателей, снятых на оборудовании        
    def activated_equip(self, text):
        if text != '': # не пустой список
            header_ind = ["Показатели", "Доп.имя"] # заголовки таблицы
            # запрос на базовые имена по оборудованию
            row_eq_ind = self.cursor.execute("SELECT Latin_name \
                                    FROM basic_name_indicator \
                                    INNER JOIN (((unit_method_equip \
                                    INNER JOIN method ON unit_method_equip.idMethod = method.idMethod) \
                                    INNER JOIN equipment ON unit_method_equip.idEquipment = equipment.idEquipment) \
                                    INNER JOIN formed_idicator_method ON method.idMethod = formed_idicator_method.idMethod) \
                                    ON basic_name_indicator.idBasicName = formed_idicator_method.idBasicName \
                                    WHERE Name_equipment = '%s'" % text)
            row_eq_ind = self.cursor.fetchall()
            # количество столбцов в таблицк
            if self.m==3 or self.check == True: # 2 столбца по условию
                self.table_equip_ind.setColumnCount(self.m-1)
            else: # 1 или 2 столбца
                self.table_equip_ind.setColumnCount(self.m)
            self.table_equip_ind.setRowCount(len(row_eq_ind)) # количество строк
            if self.m >= 1:
                for i in range(len(row_eq_ind)):
                    name_eq_1 = row_eq_ind[i][0] # базовое имя
                    new_eq_item_1 = QtWidgets.QTableWidgetItem(name_eq_1) # ячейка
                    new_eq_item_1.setFlags(QtCore.Qt.ItemIsEnabled) # запрещаем редактировать
                    self.table_equip_ind.setItem(i, 0, new_eq_item_1) # добавляем в первый столбец
                    
                    row_color_ind_eq = self.cursor.execute("SELECT idSystem \
                                         FROM basic_name_indicator \
                                         WHERE Latin_name = '%s'" \
                                         % name_eq_1)
                    row_color_ind_eq = self.cursor.fetchall()
                    color_ind = row_color_ind_eq[0][0]
                    self.table_equip_ind.item(i, 0).setBackground(QColor(self.color_orig[color_ind-1][0]*255,
                                                                         self.color_orig[color_ind-1][1]*255,self.color_orig[color_ind-1][2]*255))
                    
                    if (self.m >= 2) and self.lang != "Латинские названия": # для нелатинских названий
                        # полное доп.название
                        name_eq_2 = self.new_vertices_label[self.origin_vs.index(row_eq_ind[i][0])]
                        new_eq_item_2 = QtWidgets.QTableWidgetItem(name_eq_2) # ячейка
                        new_eq_item_2.setFlags(QtCore.Qt.ItemIsEnabled) # запрещаем редактировать
                        self.table_equip_ind.setItem(i, 1, new_eq_item_2) # добавляем во 2 столбце
                #self.table_equip_ind.horizontalHeader().setStretchLastSection(True)
                # автоматические подбор ширины столбца
                self.table_equip_ind.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                self.table_equip_ind.horizontalHeader().setMinimumSectionSize(0)
                # подписи к графикам
                if self.m == 1:
                    self.table_equip_ind.setHorizontalHeaderLabels(header_ind[:1])
                elif self.lang != "Латинские названия" and self.m >= 2 :
                    self.table_equip_ind.setHorizontalHeaderLabels(header_ind[:])
                    
    def saveas_file(self): #сохранить изображение как (смена имени или выбор другой папки)
        #выбор папки и имени для сохранения
        self.photo = QPixmap(ImageQt.toqpixmap(self.image.resize(self.bbox))) #изображение pixmap
        self.name = QFileDialog.getSaveFileName(self, 'Сохранить как', '', "*.png")[0]
        self.image.save(self.name) #сохранить под новым именем
        QMessageBox.information(self, 'Сообщение', "Ваше изображение сохранено")
        
#вызов окна 
if __name__ == '__main__': 
   app = QApplication(sys.argv) 
   form = Main() 
   form.show() 
   app.exec() 