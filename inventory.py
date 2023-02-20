#import attrgetter to find highest and smallest values of objects
from operator import attrgetter

#========The beginning of the class==========
class Shoe:

    #this constructor creates the objects
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    #str method to make data readable in same format as inventory storage
    def __str__(self):
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"

    #gets cost for shoe after receiving code name
    def get_cost(self, code):
        if code == self.code:
            print(f"\nThe cost of {self.product} is {self.cost} per unit.")

    # gets cost for shoe after receiving code name
    def get_quantity(self, code):
        if code == self.code:
            print(f"\nThe quantity in stock of {self.product} is {self.quantity}.")

#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
shoe_object_list = []
#==========Functions outside the class==============
def read_shoes_data():
    """
    Function opens inventory file, creates list of all text contained, gets length of list and then slices off
    the first line. It then replaces the new line escape character in each line with nothing, thereby deleting it.
    It then splits each line which is now a list item into a smaller list, makes a string from each using slicing,
    then calls the Shoe class on the organised data and appends to shoe object list to create all objects.
    try / except used in case the inventory file has been accidentally editied, notifies user of error but continues program.
    """
    all_data_list = []

    with open("inventory.txt", "r") as invent:
        all_text_list = invent.readlines()
        max_index = len(all_text_list)
        all_data_list_n = all_text_list[1:max_index:]

        for item in all_data_list_n:
            item = item.replace('\n', '')
            all_data_list.append(item)

        for shoe_list_item in all_data_list:
            try:
                indiv_shoe_split = shoe_list_item.split(",")

                country = indiv_shoe_split[0]
                code = indiv_shoe_split[1]
                product = indiv_shoe_split[2]
                cost = int(indiv_shoe_split[3])
                quantity = int(indiv_shoe_split[4])
            except:
                if ValueError:
                    print("Error in file reading from inventory, information incorrect, please contact support.")

            shoe_for_append = Shoe(country, code, product, cost, quantity)
            shoe_object_list.append(shoe_for_append)


def capture_shoes():
    """
    Gets information from user about shoe, combines to 1 variable, then appends to shoe object list, as well as
    writing to inventory.
    """
    new_country = input("Where is the shoe? ")
    new_code = input("What is the code for the shoe? ")
    new_product_name = input("What is the product name of the shoe? ")
    new_cost = int(input("What is the cost of the shoe? "))
    new_quantity = int(input("How many of the shoes are in stock? "))

    new_shoe_for_append = Shoe(new_country, new_code, new_product_name, new_cost, new_quantity)
    shoe_object_list.append(new_shoe_for_append)
    with open("inventory.txt", "a") as app_invent:
        file_app_new_shoe = str(new_shoe_for_append)
        app_invent.write("\n" + file_app_new_shoe)


def view_all():
    """
    Prints information about all objects in inventory.
    """
    for shoe_object in shoe_object_list:
        print(f"Product name:     {shoe_object.product}\n"
              f"Product code:     {shoe_object.code}\n"
              f"Product cost:     {shoe_object.cost}\n"
              f"Product country:  {shoe_object.country}\n"
              f"Product quantity: {shoe_object.quantity}\n")


def re_stock():
    """
    Finds lowest item in stock and offers to increase it, then writes to file.

    First uses attrgetter to find the lowest quantity in object list and store as variable.
    The information about object is shown to user and asked if they want to restock or not.
    If yes, a while loop that asks what quantity should be added, and then the number is combined with the current amount in stock.
    After this, the inventory is opened, and because __str__ has been used to imitate the original file format, all
    of the previous information is written over from the object list in exactly the way it was there originally with updated data.
    elif is used if the user says no and ends the function, and else is used if an incorrect input is entered.
    """
    lowest_quant = min(shoe_object_list, key=attrgetter("quantity"))
    restock_decision = input(
        f"Product '{lowest_quant.product}' has the lowest quantity at {lowest_quant.quantity} so should be restocked."
        f" Would you like to restock? Enter 'yes' or 'no'")
    while True:
        if restock_decision.lower() == "yes":
            re_stock_amount = int(input(f"How many extra pairs of shoes should be added to {lowest_quant.product}? "))
            lowest_quant.quantity = lowest_quant.quantity + re_stock_amount
            with open("inventory.txt", "w") as ifw:
                ifw.write("Country,Code,Product,Cost,Quantity\n")
                for object in shoe_object_list:
                    obj_for_write = str(object)
                    ifw.write(obj_for_write + "\n")
                break

        elif restock_decision.lower() == "no":
            break

        else:
            restock_decision = input("Incorrect input, please try again: ")


def search_shoe():
    """
    This function gets a code from the user and then searches the shoe object list to see if it is equal to the codes of
    shoe objects. If it is found to be equal, it prints the shoe object.
    """
    code_for_search = input("Enter the code of the shoe you would like to search for: ")
    for shoe_object in shoe_object_list:
        if code_for_search == shoe_object.code:
            print(f"Product name:     {shoe_object.product}\n"
                  f"Product code:     {shoe_object.code}\n"
                  f"Product cost:     {shoe_object.cost}\n"
                  f"Product country:  {shoe_object.country}\n"
                  f"Product quantity: {shoe_object.quantity}\n")


def value_per_item():
    """calculates value for all objects in shoe object list and prints to console"""
    for value_shoe_object in shoe_object_list:
        value = value_shoe_object.cost * value_shoe_object.quantity
        print(f"{value} is the total value of the product '{value_shoe_object.product}'")



def highest_qty():
    """
    Uses attrgetter to find max quantity from object list and prints it to console
    """
    highest_quant = max(shoe_object_list, key=attrgetter("quantity"))
    print(f"Product '{highest_quant.product}' has the highest quantity at {highest_quant.quantity} so should be put on sale.")



#==========Main Menu=============
#generate object list before menu opened
read_shoes_data()

#display options to user in while loop
while True:
    menu = input('''\nSelect one of the following Options below:
gc - Get cost
gq - Get quantity
as - Add shoes
va - View all
rs - Restock 
ss - Search shoe
vpi - Get total value of product stock
hq - Find highest quantity of stock
q - Quit program
: ''').lower()

    #get ID request and call get cost method
    if menu == "gc":
        get_cost_id = input("\nEnter the ID of the shoe you would like the cost of: ")
        for gc_obj in shoe_object_list:
            gc_obj.get_cost(get_cost_id)

    #get ID request and call get quantity method
    elif menu == "gq":
        get_quant_id = input("\nEnter the ID of the shoe you would like to know the quantity in stock of: ")
        for gq_obj in shoe_object_list:
            gq_obj.get_quantity(get_quant_id)

    #call capture shoes function
    elif menu == "as":
        capture_shoes()

    #calls view all
    elif menu == "va":
        view_all()

    #calls restock function
    elif menu == "rs":
        re_stock()

    ##call search shoe function
    elif menu == "ss":
        search_shoe()

    #calls value per item function
    elif menu == "vpi":
        value_per_item()

    #calls highest quantity method
    elif menu == "hq":
        highest_qty()

    #ends program with break
    elif menu == "q":
        break

    #displays error message if incorrect input entered
    else:
        print("Incorrect input, please try again: ")
