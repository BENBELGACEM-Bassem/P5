"""This module is responsible for defining menus for user experience"""

from dbexplorer import UseCase


class Application:
    """this class defines the user experience through a series of menus"""

    def __init__(self):
        """Initialise user choices"""
        self.first_choice = None
        self.second_choice = None
        self.third_choice = None

    def start_menu(self):
        """Start the application"""
        print('hello')
        while True:
            try:
                self.first_choice = int(
                    input(
                        "Please enter a number corresponding to one "
                        "of these options:\n"
                        "1 - Quel aliment souhaitez-vous remplacer ?\n"
                        "2 - Retrouver mes aliments substitués\n"
                        "3 - Quitter\n"))
            except ValueError:
                print("Your selection is not a number ! ")
            else:
                if self.first_choice not in (1, 2, 3):
                    print("Your choice does not belong to suggested list")
                elif self.first_choice == 3:
                    print("Au revoir")
                    break
                elif self.first_choice == 2:
                    print(UseCase.display_favourite_table())
                elif self.first_choice == 1:
                    self.categories_menu()

    def categories_menu(self):
        """Launch choosing a category"""
        categories = UseCase.display_categories()
        display_list = categories[0]
        id_list = categories[1]
        while True:
            try:
                self.second_choice = int(
                    input(
                        "Please enter an id number corresponding "
                        "to the category of your choice,\n"
                        "or choose 1 to go back to the start_menu:\n"
                        "1 - Start_menu\n"
                        f"{display_list}\n"))
            except ValueError:
                print("Your selection is not a number ! ")
            else:
                if self.second_choice == 1:
                    break
                elif self.second_choice not in id_list:
                    print('Your choice does not belong to suggested list')
                elif self.second_choice in id_list:
                    self.unhealthy_products_menu()

    def unhealthy_products_menu(self):
        """Launch products choosing menu"""
        products = UseCase.display_products(self.second_choice)
        display_list = products[0]
        barcode_list = products[1]
        while True:
            try:
                self.third_choice = int(
                    input(
                        "Please enter a barcode number corresponding "
                        "to the product of your choice,\n"
                        "or choose 1 to go back to the categories_menu:\n"
                        "1 - Catgories_menu\n"
                        f"{display_list}\n"))
            except ValueError:
                print("Your selection is not a number ! ")
            else:
                if self.third_choice == 1:
                    break
                elif self.third_choice not in barcode_list:
                    print('Your choice does not belong to suggested list')
                elif self.third_choice in barcode_list:
                    self.substitute_product_menu()

    def substitute_product_menu(self):
        """Display a substitute and propose to save it"""
        substitute = UseCase.find_substitute(self.third_choice)
        display_substitute = substitute[0]
        substitue_instances = substitute[1]
        while True:
            try:
                self.fourth_choice = int(
                    input(
                        "Below is a healthy substitute for the product "
                        "you have selected\n"
                        "Please select 1 if you want to save it "
                        "in your favourite list,\n"
                        "or 2 to go back to unhealthy product menu\n"
                        f"{display_substitute}\n"
                        "1 - Save\n"
                        "2 - unhealthy_products_menu\n"))
            except ValueError:
                print("Your selection is not a number ! ")
            else:
                if self.fourth_choice == 1:
                    UseCase.save(*substitue_instances)
                    break
                elif self.fourth_choice == 2:
                    break
                elif self.fourth not in (1, 2):
                    print('Your choice does not belong to suggested list')