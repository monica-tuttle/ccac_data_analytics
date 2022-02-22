# -*- coding: utf-8 -*-
"""

 Monica Tuttle
 10/4/2020
 Python 1 - DAT-119 - Fall 2020
 Homework assignment 5, problem 2
 
 This program averages a set of grades that is entered by the user.
 
"""
# Here we greet the user and explain what the program does.

print("Welcome to the grade averaging program!")
print("You'll enter as many grades as you want averaged;")
print("when finished, enter the number -1.")

# Here we initialize the counter and another variable that will sum up the values entered.

count = 0
sum = 0

# Here we get the user's input in the form of a whole number between 0 and 100 or -1 as a sentinel value.

user_input = int(input("Please enter a grade between 0 and 100 or the number -1: "))

# Here we will run a while loop that will do a conditional check and then accumulate values to caculate an average.

while user_input != -1:  
    if user_input <= 100 and user_input >= 0:  
        sum = sum + user_input 
        count = count + 1
    else:
        print("I'm sorry, that was not a valid input.")
        
# Here we ask the user to enter another value if it was determined that the last input was invalid.

    user_input = int(input("Please enter a grade between 0 and 100 or the number -1: "))

# Here we check to see the count is NOT going to be 0, and then we calculate the average.

if count > 0: 
    print("The average of the grades you've entered is: ", format(sum/count, '.1f'), sep = "")