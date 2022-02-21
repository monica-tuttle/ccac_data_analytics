'''
 Monica Tuttle
 11/27/2020
 Python 1 - DAT-119 - Fall 2020
 Homework assignment 10
 
 A todo list application with the ability to save items to mark off later.

Functionality:
1) add an item
2) view the items that need to be done
3) mark an item done (requires a way to get the choice from them)
4) view the items that have been completed
5) give the user a menu of choices
    
'''
import os

# our main/top-level menu
# this is a constant that we will NEVER CHANGE,
# which means making it global isn't super bad or dangerous

THE_MENU = ["View the items on your todo list", \
            "View the items you have finished", \
            "Add an item to the todo list", \
            "Mark a todo list item as completed", \
            "Exit the Todo List Application (your list will not be saved)"]


def view_list(the_list):
    """pass in a list, and this function displays it"""
    
    # a nice thing is to let the user know the program is still working
    # but there is nothing in their list
    
    if len(the_list) == 0:
        print("\nThere is nothing to display.")
        
    # count lets us put the number before the list item
    
    count = 0
    for item in the_list:
        # we start at 1 because humans are using our program
        count = count + 1 
        print(count, ") ", item, sep="")
        
    # returns nothing, and that's OK; it just prints


def get_menu_option(the_list):
    """pass in a list, and this function gets the user's choice of menu item
       (returns a list index, counting from zero, not the user's actual choice)"""
        
    # show the user their list of options
    
    print("") # just give ourselves a little space
    
    view_list(the_list)

    # if there are items in the list, get the user's choice
    
    if len(the_list) > 0:
        # get the user's choice
        
        choice = input("\nPlease choose one of the options above: ")
        if choice.isnumeric():
            choice = int(choice)
        else:
            choice = 0
        while choice < 1 or choice > len(the_list):
            print("\nI'm sorry, that wasn't one of the available options.\n")
            view_list(the_list)
            choice = input("\nPlease choose one of the options above: ")
            if choice.isnumeric():
                choice = int(choice)
            else:
                choice = 0
        # this gives you an index you can use on the list
        # (translated from human--start at 1--to computer--start at 0)
        
        return choice - 1
    # if there are no items in the list, return -1
    else: 
        return -1


def add_an_item(the_list, item):
    """takes a list and a string to be added to the list, returns nothing"""
    the_list.append(item)


def remove_an_item(the_list, item):
    """takes a list and a string to be removed from the list, returns nothing"""
    the_list.remove(item)


def mark_item_completed(todo_list, done_list):
    """takes two lists as parameters;
       removes an item from one list (presumably the todo list)
       and adds it to another list (presumably the completed item list)"""
       
    index = get_menu_option(todo_list)
    if index != -1: # if there's actually something in the list
        add_an_item(done_list, todo_list[index])
        remove_an_item(todo_list, todo_list[index])
    else:
        print("\nThere is nothing to mark completed.")


def main():
    '''control logic for the program'''
    
    # will be True if the file is there, False if not
    if os.path.isfile('todo_app_todo.txt'):
        my_file_object = open("todo_app_todo.txt", "r")
        
        # converts the text into a list
        todo_list_saved = my_file_object.readlines()
        
        # gets rid of extra newlines
        for index in range(len(todo_list_saved)):
            todo_list_saved[index] = todo_list_saved[index].strip("\n")
            
        print(todo_list_saved)
        my_file_object.close()
    else: 
        # creates a new list if the file is not found
        todo_list_saved = []
        print(todo_list_saved)
    
    # same as above but for the "completed" list
    if os.path.isfile('todo_app_done.txt'):
        my_file_object_2 = open("todo_app_done.txt", "r")
        done_list_saved = my_file_object_2.readlines()
        for index in range(len(done_list_saved)):
            done_list_saved[index] = done_list_saved[index].strip("\n")
            
        print(done_list_saved)
        my_file_object_2.close()
    else:
        done_list_saved = []
        print(done_list_saved)
        
    # set up our variables; two empty lists and a loop controller
    keep_going = True
    # greet the user
    
    
    print("Welcome to the Todo List Application.")
    # until the user chooses "exit," we keep going
    
    while keep_going:
        # get their choice from the main menu
        option = get_menu_option(THE_MENU)
        if option == 0: # view todo list
            print("\nThis is your todo list:")
            view_list(todo_list_saved)
            input("\nHit enter when finished viewing ")
        elif option == 1: # view finished list
            print("\nThis is your list of completed tasks.")
            view_list(done_list_saved)
            input("\nHit enter when finished viewing ")
        elif option == 2: # add item
            to_add = input("\nWhat would you like to add? ")
            add_an_item(todo_list_saved, to_add)
        elif option == 3: # move item to done list
            print("\nChoose an item to mark completed.")
            mark_item_completed(todo_list_saved, done_list_saved)
        else: # quit
            print("\nThank you for using the Todo List Application.")
            keep_going = False

    # writes user's added inputs to the todo list and saves them
    
    my_file_object_3 = open("todo_app_todo.txt", "w")
    for thing in todo_list_saved:
        my_file_object_3.write(thing + "\n")
    my_file_object_3.close()
    
    # writes todo list items moved to the done list and saves them
    
    my_file_object_4 = open("todo_app_done.txt", "w")
    for thing in done_list_saved:
        my_file_object_4.write(thing + "\n")
    my_file_object_4.close()
            
    # the magic that makes the program go
if __name__ == '__main__':
    main()


