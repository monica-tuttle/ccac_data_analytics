# -*- coding: utf-8 -*-
"""
 Monica Tuttle
 11/10/2020
 Python 1 - DAT-119 - Fall 2020
 Homework assignment 9
 
 A program that translates an excerpt from "Pride and Prejudice" into Pig Latin.
 
"""
# Here we import a module that allows us to do more things with strings.

import os 
import string


def get_text(filename):
    
    """get the text from the specified file, with its path passed in as a string"""
   
    the_text = ""
    
    # is the file actually there?
    
    if os.path.isfile(filename):
        
        # open it, and read its contents
        
        file_handler = open(filename, 'r')
        the_text = file_handler.read()
    return the_text


def break_into_list_of_words(the_string):
    
    """takes a long string and returns a list of all of the words in the string"""
    
    # start with an empty list to iterate through
    
    list_of_words = []
    
    # split a longer text into separate lines
    
    list_of_lines = the_string.splitlines()
    
    # split a list of lines into separate words
    
    for line in list_of_lines:
        line = line.split(' ')
        #small list of strings
        for word in line: 
            list_of_words.append(word)
            
    # strips the text of all punctuation
    
    for index in range(0, len(list_of_words)):
        list_of_words[index] = list_of_words[index].strip(';')
        list_of_words[index] = list_of_words[index].strip('\"')
        list_of_words[index] = list_of_words[index].strip('\'')
        list_of_words[index] = list_of_words[index].strip('.')
        list_of_words[index] = list_of_words[index].lower()
        list_of_words[index] = list_of_words[index].strip('?')
        list_of_words[index] = list_of_words[index].strip(',')
        list_of_words[index] = list_of_words[index].strip('!')
        list_of_words[index] = list_of_words[index].strip('\."')
        
    return list_of_words


def main(): 
    '''control logic for the program'''
    PREJUDICE = get_text('prejudice.txt')
    pig_latin_list = []
    word_list = break_into_list_of_words(PREJUDICE)
    
    # for loop that translates the text into pig latin
    
    for word in word_list:
        if len(word) == 0:
            pig_latin_list.append(" \n\n")
        else:
            pig_latin_word = word[1:] + word[0] + "ay "
            pig_latin_list.append(pig_latin_word)
    
    # converts the pig_latin_list into a string
    
    pig_latin_string = "".join(pig_latin_list)
    print(pig_latin_string)
  
    
main()
