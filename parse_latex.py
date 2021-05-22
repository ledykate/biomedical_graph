# -*- coding: utf-8 -*-
"""
Created on Fri May  7 10:39:20 2021

@author: Катрина
"""

def parse_latex(string_latex):
    # символы и скобки
    delete_symbol = ['%','`','~','!','$','^','|','&','*','_','+','-','(',')',
                     '{','}','[',']','=',',','.','\\','/']
    # определённые операторы latex
    delete_sequence = [r'\frac',r'\cfrac',r'\cdot',r'\times',r'\sqrt',
                       r'\right',r'\left']
    # нижние индексы, которые часто встречаются в нижнем регистре
    delete_index_low = ['max','min','ср','n','m']
    # удаление значений до знака =, включая его
    string_latex = string_latex.split('=', 1)[1].lstrip()
    for i in delete_sequence: # удаление операторов latex и замена их на пробел
        string_latex = string_latex.replace(i, ' ')
    for j in delete_symbol: # удаление символов и скобок и замена их на пробел
        string_latex = string_latex.replace(j, ' ')
    for h in delete_index_low: # удаление индексов в нижнем регистре
        string_latex = string_latex.replace(h, ' ')
    
    result = string_latex.split(' ') # разбитие строки по разделителю пробел
    r_empty = '' # пустое значение
    while r_empty in result: # пока в массиве есть пустой элемент
        result.remove(r_empty) # удалим его
    result = [r for r in result if not r.isdigit()] # удаление чисел
    # выделить только уникальные значения (если вдруг есть повторения)
    result = list(set(result)) 
    return(result) # результат

#### ПРОВЕРКА РАБОТЫ ФУНКЦИИ

str_lat = r'$ИМТ=\frac{МТ}{{{ДТ}^{2}}}$'
res = parse_latex(str_lat)


        
