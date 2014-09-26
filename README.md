Sentence-Generator
==================

Randomly generate phrases, sentences, and queries. This can be used to generate test set for Automatic Speech Recognition (ASR).

Usage: python run_generator.py <num-of-scripts-to-generate>
Scripts save directory: output/

Configuration: generation.conf
Configuration file format: \<SENTENCE_TYPE\>;\<DESCRIPTION\>;\<NUMBER_OF_SENTENCES\>

Available SENTENCE_TYPE:

[NUMBER, TIME, DAY_OF_WEEK , DATE, PHONE_NUMBER, NAME_WITH_PHONE_NUMBER, NAME, STREET_ADDRESS, BAY_AREA_ADDRESS, QUERY, SENTENCE]

Contact: Bing Liu, v.bingliu@gmail.com
