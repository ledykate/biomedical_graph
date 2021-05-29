# import MySQLdb
from parse_latex import parse_latex


def syst_ind(systems_ind):
    systems_ind = tuple(systems_ind)  # преобразуем список систем в кортеж
    if len(systems_ind) == 1:  # если всего одна система
        systems_ind = str(systems_ind)  # преобразуем в строку
        systems_ind = systems_ind.replace(',', '')  # удаляем запятую
    else:  # иначе
        systems_ind = str(systems_ind)  # преобразуем в строку
    return systems_ind


def my_indicator(systems_ind, cursor):
    # все латинские имена
    row_all_lat = cursor.execute("SELECT Latin_name \
                                 FROM basic_name_indicator \
                                 WHERE idSystem IN %s" % syst_ind(systems_ind))
    row_all_lat = cursor.fetchall()

    all_latin_name = []  # массив с латинскими именами
    # добавление в массив всех элементов запроса
    for i in range(len(row_all_lat)):
        all_latin_name.append(row_all_lat[i][0])
    n = len(all_latin_name)  # количество всех показателей
    return n, all_latin_name


def my_graph(all_latin_name, cursor):
    vertices_label = []  # названия вершин
    color_vs = []  # цвета вершин
    for i in range(len(all_latin_name)):
        color_vs.append([0, 0.749, 1])  # цвет у вершин голубой
    n = len(all_latin_name)  # количество всех показателей
    rows = cursor.execute("SELECT Latin_name, Calculation_form \
                                FROM (basic_name_indicator \
                                INNER JOIN unit_form_basic \
                                ON basic_name_indicator.idBasicName \
                                = unit_form_basic.idBasicName) \
                                INNER JOIN formula\
                                ON unit_form_basic.idFormula = formula.idFormula \
                                ORDER BY idUnit_form_basic;")
    rows = cursor.fetchall()  # получение данных из запроса

    # определение массивов
    base_name = []  # базовое имя
    formula_latex = []  # формула
    ##### РАСПРЕДЕЛЕНИЕ ПО МАССИВАМ
    # для каждой строки запроса
    for i in range(len(rows)):
        base_name.append(rows[i][0])  # базовое имя
        formula_latex.append(parse_latex(rows[i][1]))  # формула

    ##### ПОИСК Латинского названия по аббревиатуре
    for i in range(len(rows)):
        for j in range(len(formula_latex[i])):
            # запрос на нахождение показателя с определённой аббревиатурой
            rows_lat = cursor.execute("SELECT Latin_name\
              FROM additional_name INNER JOIN basic_name_indicator \
              ON additional_name.idBasicName = basic_name_indicator.idBasicName \
              WHERE Abbreviation_add_name = '%s'" % formula_latex[i][j])
            rows_lat = cursor.fetchall()  # получение данных из запроса
            if len(rows_lat) != 0:  # если запрос не пустой
                formula_latex[i][j] = rows_lat[0][0]  # заменяем аббревиатуру на латинское название
            else:
                formula_latex[i][j] = ''  # если не нашёл, то пустой
        # оставляем только не пустые значения
        formula_latex[i] = [ind for ind in formula_latex[i] if ind != '']

    edges_graph = []  # массив с рёбрами (кортежы)
    for i in range(n):  # для всех показателей
        for j in range(len(base_name)):  # для показателей, которые имеют формулу
            if all_latin_name[i] == base_name[j]:  # если совпадают
                # формула не пустая (в БД есть показатели из формулы)
                if (len(formula_latex[j])) != 0:
                    for h in range(len(formula_latex[j])):  # для каждого аргумента
                        # находим индекс показателя
                        if formula_latex[j][h] in all_latin_name:
                            m = all_latin_name.index(formula_latex[j][h])
                            edges_graph.append((i, m))  # добавляем ребро

    vertices_label += all_latin_name  # добавляем в подписи к вершинам
    '''
    ##### ПОКАЗАТЕЛИ, ФОРМИРУЕМЫЕ ПО МЕТОДИКЕ--------------------------------------
    # запрос, которые выводит всю таблицу formed_idicator_method, но
    # вместо id показатели и методики выводит латинское название показателя
    # и название методики на русском языке
    for i in range(len(vertices_label)):
        # запрос по нахождению методики по названию
        row_meth_ind = cursor.execute("SELECT Name_method_Russian \
                                  FROM (formed_idicator_method \
                                  INNER JOIN basic_name_indicator \
                                  ON formed_idicator_method.idBasicName = \
                                  basic_name_indicator.idBasicName) \
                                  INNER JOIN method \
                                  ON formed_idicator_method.idMethod = \
                                  method.idMethod \
                                  WHERE Latin_name = '%s'" % vertices_label[i])
        row_meth_ind = cursor.fetchall()
        if row_meth_ind != ():
            for j in range(len(row_meth_ind)):
                if row_meth_ind[j][0] not in vertices_label: # если нет в списке
                    vertices_label.append(row_meth_ind[j][0]) # добавляем вершину
                    color_vs.append([0,1,0]) # цвет методик зелёный
                edges_graph.append((i,vertices_label.index(row_meth_ind[j][0]))) # добавляем ребро
    m = len(vertices_label)
    
    #### МЕТОДИКИ И ОБОРУДОВАНИЕ, НА КОТОРОМ ОНИ ИЗМЕРЯЮТСЯ------------------------  
    # запрос таблицы unit_method_equip, но выводятся название оборудования
    for i in range(n,m): # для каждой методики
        # находим оборудование, на котором измеряется
        rows_met_eq = cursor.execute("SELECT Name_equipment \
                                     FROM (unit_method_equip \
                                           INNER JOIN method \
                                           ON unit_method_equip.idMethod = \
                                           method.idMethod) \
                                     INNER JOIN equipment \
                                     ON unit_method_equip.idEquipment = \
                                     equipment.idEquipment \
                                     WHERE method.Name_method_Russian = '%s'" \
                                     % vertices_label[i])
        rows_met_eq = cursor.fetchall()
        if rows_met_eq != (): # елси запрос не пустой
            for j in range(len(rows_met_eq)):
                if rows_met_eq[j][0] not in vertices_label: # в списке вершин
                    vertices_label.append(rows_met_eq[j][0]) # добавляем вершину
                    color_vs.append([1,1,0]) # цвет вершины оборудования - жёлтый
                edges_graph.append((i,vertices_label.index(rows_met_eq[j][0]))) # добавляем ребро
                    
    '''
    return n, vertices_label, color_vs, edges_graph


##### ПРОВЕРКА РАБОТЫ ФУНКЦИИ
'''
systems_ind = [1,2]
conn = MySQLdb.connect('localhost', 'root', 'root','biomedical_indicators',charset='utf8', 
                       use_unicode = True)
cursor = conn.cursor()
n, vertices_label, color_vs, edges_graph = my_graph(systems_ind,cursor)

print("Список вершин")
print(vertices_label)
print("Список рёбер")
print(edges_graph)
'''
