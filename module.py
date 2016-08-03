# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 18:04:18 2014

@author: Bing Liu
"""

import functions
from random import random
from random import randint
import datetime
import re
import os
    
class sentence_generator:     
    root_dir = os.path.dirname(os.path.abspath(__file__))
    queries = functions.read_list(root_dir + '/data/queries.txt')
    real_bay_area_address = functions.read_list(root_dir + '/data/bay_area_addresses.csv')
    street_names = functions.read_weighted_dict(root_dir + '/data/us_street_name_sorted_top75percent.csv')
    city_names = functions.read_list(root_dir + '/data/us_cities.csv')
    state_names = functions.read_list(root_dir + '/data/us_states.csv')
    # Function def: read_person_names(file_name. accumulated prob threshold)
    female_first_names = functions.read_person_names(root_dir + '/data/dist.female.first', 10)
    male_first_names = functions.read_person_names(root_dir + '/data/dist.male.first', 10)
    last_names = functions.read_person_names(root_dir + '/data/dist.all.last', 10)
    day_of_week = functions.read_list(root_dir + '/data/DAY-OF-WEEK.vocab')
    person_famous = functions.read_list(root_dir + '/data/PERSON-FAMOUS.vocab')
    restaurant_types = functions.read_list(root_dir + '/data/RESTAURANT-TYPE.vocab')
    restaurant_food = functions.read_list(root_dir + '/data/RESTAURANT-FOOD.vocab')
    restaurant_names = functions.read_list(root_dir + '/data/RESTAURANT-NAME.vocab')
    retailers = functions.read_list(root_dir + '/data/RETAILER.vocab')
    websites = functions.read_list(root_dir + '/data/WEBSITE.vocab')
    sentences = functions.read_list(root_dir + '/data/sentences.txt')
    story_sentences = functions.read_list(root_dir + '/data/story_sentences.txt')
        
    time_format = dict()
    time_format['%I:%M %p'] = 0.6       # e.g. '10:40 AM'
    time_format['%I:%M'] = 0.4          # e.g. '06:35'
    
    date_format = dict()
    # replaced %d with {d}, so as to add prefix (th, st, nd, rd) in generate_date function
    date_format['%A, %B {d}'] = 0.5     # e.g. 'Sunday, November 19th'
    date_format['%B {d}'] = 0.3         # e.g. 'March 11th'
    date_format['{d} of %B'] = 0.2      # e.g. '24th of December'
        
    # define weights for number of digits to be generated for street numbers
    num_digit = dict()
    num_digit[1] = 9
    num_digit[2] = 90
    num_digit[3] = 100
    num_digit[4] = 100
    
    
    time_format = dict()
    time_format['%I:%M %p'] = 0.6 # e.g. '10:40 AM'
    time_format['%I:%M'] = 0.4 # e.g. '06:35'
    
    def generate_time(self):
        """ Generate random time
        Format is configured in time_format variable
        Sample output: '10:40 AM', '03:17 PM', '06:35'
        """
        dt = datetime.datetime(2000, 01, 01, randint(0,23), randint(0,11)*5)
        time_str = dt.strftime(functions.weighted_random(self.time_format))
        if (time_str[0] == '0'):
            time_str = time_str[1:]
        return time_str
    
    
    def suffix(self, d):
        return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')
    
    def custom_strftime(self, format, t):
        return t.strftime(format).replace('{d}', str(t.day) + self.suffix(t.day))
    
    
    date_format = dict()
    # replaced %d with {d}, so as to add prefix (th, st, nd, rd) in generate_date function
    date_format['%A, %B {d}'] = 0.5     # e.g. 'Sunday, November 19th'
    date_format['%B {d}'] = 0.3         # e.g. 'March 11th'
    date_format['{d} of %B'] = 0.2      # e.g. '24th of December'
    
    def generate_date(self):
        """ Generate random date
        Format is configured in date_format variable
        Sample output: '10:40 AM', '03:17 PM', '06:35'
        """    
        dt = datetime.datetime(2000, randint(1,12), randint(1,29))
        date_str = self.custom_strftime(functions.weighted_random(self.date_format), dt)
        # date_str = dt.strftime(weighted_random(date_format))
        return date_str
    
    def generate_street_num(self, num_digit):
        street_num = ''    
        for i in range(num_digit):
            if (i == 0):
                digit = randint(1, 9)
            else:
                digit = randint(0, 9)
            street_num += str(digit)
        return street_num
    
    def generate_street_name(self):
        street_name_with_num = self.generate_street_num(functions.weighted_random(self.num_digit)) + ' ' + functions.weighted_random(self.street_names)
        # add city_state_name with 30% and 10% prob
        city_state_name = ''
        rand_num = random()
        if (rand_num < 0.3):
            city_state_name = city_state_name + ', ' + functions.random_ele(self.city_names)
            if (rand_num < 0.1):
                city_state_name = city_state_name + ', ' + functions.random_ele(self.state_names)
        return street_name_with_num + city_state_name
    
    def generate_bay_area_address(self):
        return functions.random_ele(self.real_bay_area_address)
    
    def generate_phone_number(self):
        phone_num = []
        for i in range (10):
            count = i + 1
            if (count == 1):
                digit = str(randint(1,9))
                phone_num.append(digit)
            elif (count == 3 or count == 6):
                digit = str(randint(0,9))
                phone_num.append(digit)
                phone_num.append('-')
            else:
                digit = str(randint(0,9))
                phone_num.append(digit)
        return ' '.join(phone_num)
        
    def generate_name_with_phone_number(self):
        actions = ['Call', 'Dail', 'Make a call to']
        name = self.generate_first_name()
        phone_num = self.generate_phone_number()
        action = actions[randint(0,len(actions)-1)]
        return action + ' %s at %s' % (name, phone_num)
    
    def generate_query(self):
        query = functions.random_ele(self.queries)
        match_subs = re.findall(r'@([^ ]+)', query)
        if len(match_subs) > 0:
            for match_term in match_subs:
                # print ('Replacing ' + match_term)
                query = re.sub(r'@' + match_term, self.generate_phrase(match_term), query).capitalize()
        return query
    
    def generate_city(self):
        return functions.random_ele(self.city_names)

    def generate_day_of_week(self):
        return functions.random_ele(self.day_of_week)
        
    def generate_person_famous(self):
        return functions.random_ele(self.person_famous)

    def generate_first_name(self):
        if (randint(0, 1)%2 == 0):
            first_name = functions.weighted_random(self.female_first_names)
        else:
            first_name = functions.weighted_random(self.male_first_names)
        return first_name
        
    def generate_last_name(self):
        last_name = functions.weighted_random(self.last_names)
        return last_name
        
    def generate_name(self):
        name = self.generate_first_name() + ' ' + self.generate_last_name()
        return name

    def generate_restaurant_type(self):
        return functions.random_ele(self.restaurant_types)

    def generate_restaurant_food(self):
        return functions.random_ele(self.restaurant_food)

    def generate_restaurant_name(self):
        return functions.random_ele(self.restaurant_names)
        
    def generate_retailer(self):
        return functions.random_ele(self.retailers)
    
    def generate_website(self):
        return functions.random_ele(self.websites)

    def generate_starting_notice(self):
        notice = list()
        notice.append('Now it\'s time to get started.') 
        notice.append('I understand that the data collected via this App will be used for development purposes.') 
        notice.append('We thank you in advance for your help.') 
        return '\n'.join(notice)

    def generate_ending_notice(self):
        notice = list()
        notice.append('This reading task is now complete, thank you for your time.') 
        return '\n'.join(notice)
        
    def generate_simple_sentences(self):
        samples = list()
        samples.append('Check for new messages.')
        samples.append('Hello.')
        samples.append('Goodbye.')        
        samples.append('Yes.') 
        samples.append('No.')
        samples.append('Help.')
        samples.append('Open Facebook.')
        samples.append('Start navigation.')
        samples.append('Create a new Email.') 
        return '\n'.join(samples)

    def generate_story_sentences(self):
        sample_length = 25
        start_index = randint(0, len(self.story_sentences) - sample_length)
        end_index = start_index + sample_length
        sample_sentences = self.story_sentences[start_index:end_index]
        return '\n'.join(sample_sentences)
        
    def generate_sentences(self):
        return functions.random_ele(self.sentences)
    
    def generate_phrase(self, phrase_type):
        phrase = ''        
        if (phrase_type == 'CITY'):
            phrase = self.generate_city()
        elif (phrase_type == 'DAY-OF-WEEK'):
            phrase = self.generate_day_of_week()
        elif (phrase_type == 'PERSON-FAMOUS'):
            phrase = self.generate_person_famous()
        elif (phrase_type == 'PERSON-FIRSTNAME'):
            phrase = self.generate_first_name()
        elif (phrase_type == 'PERSON-LASTNAME'):
            phrase = self.generate_last_name()
        elif (phrase_type == 'RESTAURANT-TYPE'):
            phrase = self.generate_restaurant_type()
        elif (phrase_type == 'RESTAURANT-FOOD'):
            phrase = self.generate_restaurant_food()
        elif (phrase_type == 'RESTAURANT-NAME'):
            phrase = self.generate_restaurant_name()
        elif (phrase_type == 'RETAILER'):
            phrase = self.generate_retailer()
        elif (phrase_type == 'TIME'):
            phrase = self.generate_time()
        elif (phrase_type == 'WEBSITE'):
            phrase = self.generate_website()
        return phrase
    
    def generate_sentence(self, sentence_type):
        sentence = ''        
        if (sentence_type == 'STARTING_NOTICE'):
            sentence = self.generate_starting_notice()
        elif (sentence_type == 'SIMPLE_SENTENCE'):
            sentence = self.generate_simple_sentences()
        elif (sentence_type == 'NUMBER'):
            sentence = self.generate_street_num(functions.weighted_random(self.num_digit))
        elif (sentence_type == 'TIME'):
            sentence = self.generate_time()
        elif (sentence_type == 'DAY_OF_WEEK'):
            sentence = self.generate_day_of_week()
        elif (sentence_type == 'DATE'):
            sentence = self.generate_date()
        elif (sentence_type == 'PHONE_NUMBER'):
            sentence = self.generate_phone_number()
        elif (sentence_type == 'NAME_WITH_PHONE_NUMBER'):
            sentence = self.generate_name_with_phone_number()
        elif (sentence_type == 'NAME'):
            sentence = self.generate_name()
        elif (sentence_type == 'STREET_ADDRESS'):
            sentence = self.generate_street_name()
        elif (sentence_type == 'BAY_AREA_ADDRESS'):
            sentence = self.generate_bay_area_address()
        elif (sentence_type == 'QUERY'):
            sentence = self.generate_query()
        elif (sentence_type == 'SENTENCE'):
            sentence = self.generate_sentences()
        elif (sentence_type == 'ENDING_NOTICE'):
            sentence = self.generate_ending_notice()        
        return sentence
