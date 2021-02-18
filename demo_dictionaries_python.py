# -*- coding: utf-8 -*-
"""

 Monica Tuttle
 10/31/2020
 Python 1 - DAT-119 - Fall 2020
 Homework assignment 8, problem 1
 
 
 A program that quizzes a user's knowledge of US state capitals.
 
"""
from random import randint


def main():
    '''control logic for the program'''
    
    # Dictionary with states & their capitals
    
    capitals = {
                'Alabama' : 'Montgomery', 
                'Alaska' : 'Juneau',
                'Arizona' : 'Phoenix', 
                'Arkansas' : 'Little Rock',
                'California' : 'Sacramento', 
                'Colorado' : 'Denver',
                'Connecticut' : 'Hartford', 
                'Delaware' : 'Dover',
                'Florida' : 'Tallahassee', 
                'Georgia' : 'Atlanta',
                'Hawaii' : 'Honolulu', 
                'Idaho' : 'Boise',
                'Illinois' : 'Springfield', 
                'Indiana' : 'Indianapolis',
                'Iowa' : 'Des Moines', 
                'Kansas' : 'Topeka',
                'Kentucky' : 'Frankfort', 
                'Louisiana' : 'Baton Rouge',
                'Maine' : 'Augusta', 
                'Maryland' : 'Annapolis',
                'Massachusetts' : 'Boston', 
                'Michigan' : 'Lansing',
                'Minnesota' : 'Saint Paul', 
                'Mississippi' : 'Jackson',
                'Missouri' : 'Jefferson City', 
                'Montana' : 'Helena',
                'Nebraska' : 'Lincoln', 
                'Nevada' : 'Carson City',
                'New Hampshire' : 'Concord', 
                'New Jersey' : 'Trenton',
                'New Mexico' : 'Santa Fe', 
                'New York' : 'Albany',
                'North Carolina' : 'Raleigh', 
                'North Dakota' : 'Bismarck',
                'Ohio' : 'Columbus', 
                'Oklahoma' : 'Oklahoma City',
                'Oregon' : 'Salem', 
                'Pennsylvania' : 'Harrisburg',
                'Rhode Island' : 'Providence', 
                'South Carolina' : 'Columbia',
                'South Dakota' : 'Pierre', 
                'Tennessee' : 'Nashville',
                'Texas' : 'Austin', 
                'Utah' : 'Salt Lake City',
                'Vermont' : 'Montpelier', 
                'Virginia' : 'Richmond',
                'Washington' : 'Olympia', 
                'West Virginia' : 'Charleston',
                'Wisconsin' : 'Madison', 
                'Wyoming' : 'Cheyenne'
                }
    
    # dissociates states from their capitals into a list of states
    
    states = list(capitals.keys())
    
    # randomizes a state selection 
    
    random_state = states[randint(0, len(states) - 1)] 
    
    # asks for user input and gives instructions on how to end the program
    
    user_input = input("What is the capital of " + random_state + "? (Or enter 0 to quit) " )
    
    # counters initialized outside of the while loop
    
    count_correct = 0
    count_incorrect = 0
    
    # shows the capital that is associated with the state randomly selected
    
    capital_name = capitals[random_state]
    
    # occurs until user quits program by pressing "0"
    
    while user_input !="0":
        
        # allows user's entry to be lowercase; disregards capitalization errors
        
        if user_input.lower() == capital_name.lower():
            
            # counter for how many times the user guesses the capital correctly
            
            count_correct = count_correct + 1
            
            # removes the random state selected after user guesses capital correctly
            
            states.remove(random_state)
            #print(states)  # this code which is current commented out, helped me debug
            
            print("That's correct.")
        else:
            
            # counter for incorrect guesses
            
            count_incorrect = count_incorrect + 1
            
            print("That's incorrect. The capital is " + capital_name, ".", sep = "")
        random_state = states[randint(0, len(states) - 1)] 
        capital_name = capitals[random_state]
        user_input = input("What is the capital of " + random_state + "? (Or enter 0 to quit) " )
    
    # ends the program and summarizes the number of correct and incorrect guesses
    
    if user_input == "0":
        print("You had", count_correct, "correct responses and", count_incorrect, "incorrect responses.")


main()
