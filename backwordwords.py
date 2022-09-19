# -*- coding: utf-8 -*-
"""
 Monica Tuttle
 10/4/2020
 Python 1 - DAT-119 - Fall 2020
 Homework assignment 5, problem 1
 
 This program makes words/sentences show as backwards and counts how many characters long they are.
"""
# Here we greet the user and ask the user for an input.

print("Welcome to the backwards-word maker!")
word = input("Please enter a word or sentence here: ")

# Here we print the output that results from a for loop that 
# rearranges the order of the characters in the string to show as backwards.

print("Reversed, it reads: ", end = "")
for index in range(len(word) - 1, - 1, - 1):
    print(word[index], end = "")
print()

# Here we tell the user how many characters long the word is.

print("The word or sentence you entered is", len(word), "characters long.")
