from collections import defaultdict
from var_text2num import *

import pandas as pd
import math
import importlib

def fix_million(parsed_l,typeed_l):
    new_parsed_l = []
    new_typeed_l = []
    for i in range(len(parsed_l)):
        e_a = parsed_l[i]
        type_a = typeed_l[i]
        if e_a == '000000' and new_typeed_l[-1] not in ['op','const','x']:
            new_parsed_l[-1] = new_parsed_l[-1]+e_a
            new_typeed_l[-1] = 'nums'
        else:
            new_parsed_l.append(e_a)
            new_typeed_l.append(type_a)
    return sum_nums(new_parsed_l, new_typeed_l)

def fix_times(parsed_l,typeed_l):
    new_parsed_l = []
    new_typeed_l = []
    for i in range(len(parsed_l)):
        e_a = parsed_l[i]
        e_b = ''
        if i+1 < len(parsed_l): e_b = parsed_l[i+1]
        type_a = typeed_l[i]
        type_b = ''
        if i+1 < len(parsed_l): type_b = typeed_l[i+1]

        new_parsed_l.append(e_a)
        new_typeed_l.append(type_a)
        if (type_a in ['num','nums', 'const','x'] or e_a in [')']) and type_b in ['const','x'] :
            new_parsed_l.append('*')
            new_typeed_l.append('op')
        if (type_a in ['num','nums', 'const','x'] or e_a in [')']) and e_b in ['('] :
            new_parsed_l.append('*')
            new_typeed_l.append('op')
    return new_parsed_l,new_typeed_l 

def sum_nums(parsed_l,typeed_l):
    new_parsed_l = []
    new_typeed_l = []
    cumulative = 0
    for i in range(len(parsed_l)):
        e_a = parsed_l[i]
        type_a = typeed_l[i]
        if type_a == 'nums':
            cumulative += float(e_a)
        else:
            if cumulative != 0:
                new_parsed_l.append(str(int(cumulative)))
                new_typeed_l.append('nums')
                cumulative = 0
            new_parsed_l.append(e_a)
            new_typeed_l.append(type_a)
    if cumulative != 0 :
        new_parsed_l.append(str(cumulative))
        new_typeed_l.append('nums')
        cumulative = 0 
    return new_parsed_l,new_typeed_l
    


def group_place(parsed_l,typeed_l):
    new_parsed_l = []
    new_typeed_l = []
    for i in range(len(parsed_l)):
        e_a = parsed_l[i]
        e_b = ''
        if i+1 < len(parsed_l): e_b = parsed_l[i+1]
        type_a = typeed_l[i]
        type_b = ''
        if i+1 < len(parsed_l): type_b = typeed_l[i+1]
        if type_a == 'pre' and type_b == 'place':
            new_parsed_l.append(e_a+e_b)
            new_typeed_l.append('nums')
        elif type_a == 'post':
            new_parsed_l.append(e_a)
            new_typeed_l.append('nums')
        elif type_a not in ['pre','place','post']:
            new_parsed_l.append(e_a)
            new_typeed_l.append(type_a)
    return new_parsed_l,new_typeed_l

oovs = []
def straight_parse(l):
    l = ['เริ่ม']+l+['คำนวณให้หน่อย']
    parsed_l=[]
    typeed_l=[]
    mem=[]
    for w,nw in zip(l,l[1:]+['คำนวณให้หน่อย']):
        # print(w,mem,text2type[w])
        try:
            if text2type[w] in ['op'] and len(mem) and mem[-1]=='ready_to_close' and w not in ['ปิดรูท','ฐาน']:
                parsed_l.append(')')
                typeed_l.append('op')
                mem = mem[:-1]
            
            parsed_l.append(text2num[w])

            if len(mem) and 'wait_num'==mem[-1] and text2num[w]=='(':
                mem[-1] = 'wait_close_bracket'
            if len(mem) and 'wait_close_bracket'==mem[-1] and text2num[w]==')':
                mem[-1] = 'ready_to_close'
            if len(mem) and 'wait_num'==mem[-1] and text2type[w] in ['num','nums','const','pre','place']:
                mem[-1] = 'ready_to_close'
            if  w=='สิบ' and len(typeed_l) and ( (typeed_l[-1] not in ['num']) or (parsed_l[-2] in ['.','000000'])):                    
                parsed_l[-1] = '1'
                typeed_l.append('pre')
                parsed_l.append('0')
                typeed_l.append('place')
            elif text2type[w]=='op_incom':
                typeed_l.append(text2type[w])
                mem.append('wait_num')
            elif len(typeed_l) and typeed_l[-1] in ['num','post'] and text2type[w]=='place' and parsed_l[-2]!='000000':
                typeed_l[-1]='pre'
                typeed_l.append('place')
            elif len(typeed_l) and typeed_l[-1] in ['place'] and text2type[w]=='num' and text2type[nw] not in ['place'] and w not in ['ล้าน','จุด']:
                typeed_l.append('post')
            else: 
                typeed_l.append(text2type[w])
        except: print('ERROR: ',w)
    for i in range(len(mem)):
        parsed_l.append(')')
        typeed_l.append('op')
    return parsed_l, typeed_l

def list2equation(l):
    parsed_l, typeed_l = straight_parse(l)
    # print(list(zip(typeed_l,parsed_l)))
    # print('----------------------')
    parsed_l, typeed_l = group_place(parsed_l,typeed_l)
    # print(list(zip(typeed_l,parsed_l)))
    # print('----------------------')
    parsed_l,typeed_l = sum_nums(parsed_l,typeed_l)
    # print(list(zip(typeed_l,parsed_l)))
    parsed_l,typeed_l = fix_million(parsed_l,typeed_l)
    # print(list(zip(typeed_l,parsed_l)))
    parsed_l,typeed_l = fix_times(parsed_l,typeed_l)
    # print(list(zip(typeed_l,parsed_l)))
    # print(''.join(parsed_l))
    return ''.join(parsed_l)

def text2ans(text):
    equation = list2equation(text.split())
    if equation.find('=') > 0 :
        zero_equation = left_minus_right(equation)
        return solve(eval(zero_equation)), equation
    else: 
        return eval(equation),equation