# -*- coding: utf-8 -*-
"""
This program is used for generating ramdom sentences and queries for Automatic Speech Recognition (ASR) model training

Created on Fri Aug 29 16:01:10 2014
@author: Bing Liu, v.bingliu@gmail.com
"""

import module
import functions
import sys
import os

def main(argv):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    generator = module.sentence_generator()
    configuration = functions.read_configuration(root_dir + '/generation.conf')
    output_dir = root_dir + '/output'
    
    print(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        total_num_output_files = int(argv[1])
    except ValueError:
        print('Error: Please enter a number.')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file_name = output_dir + '/combined_script.txt'
    f_w_combined = open(output_file_name, 'wb')
    for i in range (total_num_output_files):
        print('Generating script No. ' + str(i+1))
        output_file_name = root_dir + '/output/script' + str(i+1) + '.txt'
        f_w = open(output_file_name, 'wb')    
        for k, v in configuration.items():
            sentence_type = k.split(':')[0]
            description = k.split(':')[1]
            sentence_count = int(v)
            f_w.write('*%s\n' % description)
            # f_w_combined.write('*%s\n' % description)
            for i in range(sentence_count):
                sentence = generator.generate_sentence(sentence_type)
                f_w.write('%s\n' % sentence)
                f_w_combined.write('%s\n' % sentence)
            f_w.write('\n')
        f_w.close()
    f_w_combined.close()

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Usage: python run_generator.py <num-of-scripts-to-generate>")
    else:
        main(sys.argv)