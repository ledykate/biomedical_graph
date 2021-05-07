# -*- coding: utf-8 -*-
"""
Created on Fri May  7 10:39:20 2021

@author: Катрина
"""

def parse_latex(string_latex):
    # символы и скобки
    delete_symbol = ['%','`','~','!','$','^','|','&','*','_','+','-','(',')','{','}','[',']','=']
    # оперделённые операторы latex
    delete_sequence = [r'\frac',r'\cfrac',r'\cdot',r'\times',r'\sqrt']
    # нижние индексы, которы часто встречаются в нижнем регистре
    delete_index_low = ['max','min','ср','n','m']
    # нижние индексы, которы часто встречаются в верхнем регистре
    delete_index_upp = [i.upper() for i in delete_index_low]
    # удаление значений до знака =, включая его
    st_latex = string_latex.split('=', 1)[1].lstrip()
    
    for i in delete_symbol: # удаление символо и скобок и замена их на пробел
        st_latex = st_latex.replace(i, ' ')
    for j in delete_sequence: # удаление операторов latex и замена их на пробел
        st_latex = st_latex.replace(j, ' ')
    for h in delete_index_low: # удаление индексов в нижнем регистре
        st_latex = st_latex.replace(h, ' ')
    for k in delete_index_upp: # удаление индексов в верхнем регистре
        st_latex = st_latex.replace(k, ' ') 
    
    result = st_latex.split(' ') # разбитие строки по разделителю пробел
    r_empty = '' # пустое значение
    while r_empty in result: # пока в массиве есть пустой элемент
        result.remove(r_empty) # удалим его
    result = [r for r in result if not r.isdigit()] # удаление чисел
    result = list(set(result)) # выделить только уникальные значения (если вдруг есть повторения)
    return(result) # результат

str_lat = r'$КВ=\frac{ЧСС_{n-1}\cdot10}{ПД}$'
res = parse_latex(str_lat)


        
