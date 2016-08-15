# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 18:04:18 2014

@author: Bing Liu
"""
from random import random
from random import randint
import collections

def read_configuration(file_name):
    f_r = open(file_name, 'rb')
    ordered_dict = collections.OrderedDict()

    for line in f_r:
        sentence_type = line.split(';')[0]
        sentence_description = line.split(';')[1]
        sentence_num = int(line.split(';')[2])   
        ordered_dict[sentence_type + ':' + sentence_description] = sentence_num
    f_r.close()
    return ordered_dict    

def weighted_random(weights_dict):
    number = random()*sum(weights_dict.values())
    for k,v in weights_dict.iteritems():
        if number < v:
            break
        number -= v
    return k

def random_ele(ele_list):
    return ele_list[randint(0, len(ele_list)-1)]

def read_weighted_dict(file_name):
    f_r = open(file_name, 'rb')
    weighted_dict = {}

    for line in f_r:
        ele = line.split('\t')[0]
        weight = float(line.split('\t')[1])   
        weighted_dict[ele] = weight
    f_r.close()
    return weighted_dict

def read_list(file_name):
    f_r = open(file_name, 'rb')
    ele_list = list()

    for line in f_r:
        ele_list.append(line.strip())
    f_r.close()
    return ele_list

def read_person_names(file_name, name_accu_prob_threshold):    
    accu_prob_threshold = name_accu_prob_threshold
    # read female first names from file
    f_r = open(file_name, 'rb')
    name_dist = {}
    
    prob = 0
    for line in f_r:
        name = line.split()[0].title()
        accu = float(line.split()[2])
        if (accu < accu_prob_threshold):
            prob = float(line.split()[1])   
        name_dist[name] = prob
    f_r.close()
    return name_dist
