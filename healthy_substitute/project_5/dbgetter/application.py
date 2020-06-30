"""This module is responsible for defining menus for user experience"""

from .dbexplorer import UseCase


class Application:
    """this class defines the user experience through a series of menus"""

    def __init__(self):
        """Initialise user choices"""
        self.first_choice = None
        self.second_choice = None
        self.third_choice = None

    def start_menu(self):
        """Start the application"""
        print('Hello')
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
        while True:
            try:
                self.second_choice = int(
                    input(
                        "Please enter an id number corresponding "
                        "to the category of your choice,\n"
                        "or choose 1 to go back to the start_menu:\n"
                        "1 - Start_menu\n"
                        f"{categories[0]}\n"))
            except ValueError:
                print("Your selection is not a number ! ")
            else:
                if self.second_choice == 1:
                    break
                elif self.second_choice not in categories[1]:
                    print('Your choice does not belong to suggested list')
                elif self.second_choice in categories[1]:
                    self.unhealthy_products_menu()

    def unhealthy_products_menu(self):
        """Launch products choosing menu"""
        products = UseCase.display_products(self.second_choice)
        while True:
            try:
                self.third_choice = int(
                    input(
                        "Please enter a barcode number corresponding "
                        "to the product of your choice,\n"
                        "or choose 1 to go back to the categories_menu:\n"
                        "1 - Catgories_menu\n"
                        f"{products[0]}\n"))
            except ValueError:
                print("Your selection is not a number ! ")
            else:
                if self.third_choice == 1:
                    break
                elif self.third_choice not in products[1]:
                    print('Your choice does not belong to suggested list')
                elif self.third_choice in products[1]:
                    self.substitute_product_menu()

    def substitute_product_menu(self):
        """Display a substitute and propose to save it"""
        substitute = UseCase.display_substitute(self.third_choice)
        while True:
            try:
                self.fourth_choice = int(
                    input(
                        "Below is a search result for a healthy substitute "
                        "for the product you have selected\n"
                        f"{substitute[0]}\n"
                        "1 - Save into your favourite list\n"
                        "2 - Back to unhealthy_products_menu\n"))
            except ValueError:
                print("Your selection is not a number ! ")
            else:
                if self.fourth_choice == 1:
                    # Save only if a substitute is found
                    if len(substitute) > 1:
                        UseCase.save(substitute[1][0])
                        print('The substitute is added to your favourite list')
                        break
                    else:
                        print('There is no product to be saved')
                        break
                elif self.fourth_choice == 2:
                    break
                elif self.fourth not in (1, 2):
                    print('Your choice does not belong to suggested list')
