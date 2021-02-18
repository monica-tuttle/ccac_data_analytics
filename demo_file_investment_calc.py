# -*- coding: utf-8 -*-
'''
 Monica Tuttle
 09/19/2020
 Python 1 - DAT-119 - Fall 2020
 Homework assignment 3, problem 1
 
 This program calculates the return on an investment after 10, 20, and 30 years.
'''
# Below we are telling the user what to expect and hard-coding constants.

print()
print("If you start with $1000 and invest it at a return of 7% for the following")
print("amounts of time, you can expect to end up with...")
PRINCIPAL = 1000
RATE_OF_RETURN = 0.07

# Used below is formula a = p x (1 + r) ^ n to calculate investments for n years.

investment_10_years = PRINCIPAL * (1 + RATE_OF_RETURN) ** 10
investment_20_years = PRINCIPAL * (1 + RATE_OF_RETURN) ** 20
investment_30_years = PRINCIPAL * (1 + RATE_OF_RETURN) ** 30

# Below is a presentation of the answers from the formula used above.

print("Amount after 10 years: ", "$" , format(investment_10_years, '.2f'), sep="")
print("Amount after 20 years: ", "$" , format(investment_20_years, '.2f'), sep="")
print("Amount after 30 years: ", "$" , format(investment_30_years, '.2f'), sep="")
    

