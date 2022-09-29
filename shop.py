"""
Items
Prices
Buying
    - potions
    - weapons
Selling?
Menu?

Menu:

_____________________
(Start)

  Available Items:
    Health Potion ($10) - type 1
    Arrows ($20) - type 2
    Leave Shop - type x
    
(Next Page)

  How many (item chosen)s would you like to buy?
  
(checks to see if the player has enough money)

(Next Page)

    You now have (new amount) of (item chosen).

  (or)

    You do not have enough money for this item. 



"""


from universal_globals import (width, height, width2, height2, floorwidth2, floorheight2, clear_screen, constrain, enter_to_continue)


"""
A dict containing everything that the player has.

item name: amount
"""
player_items = {
    'money': 1000,  # Completely arbitrary amount
    'arrows': 0,
}

def update_player_item(name, amount):
    if name in player_items:
        player_items[name] += amount
    else:
        player_items.update({name: amount})


def set_player_item(name, amount):
    if name in player_items:
        player_items[name] = amount
    else:
        player_items.update({name: amount})


class Shop:
    """
    This class had methods that handle all the interactions while in a shop scene.
    """

    def __init__(self, items):
        # item name : cost
        self.items = items

    def _get_choice(self, choice):
        """Get, evaluate, and format which item the player wants"""
        
        # The following adds a little readability when accessing items
        name = 0
        cost = 1
        supply = 2

        while choice not in [str(x + 1) for x in range(len(self.items))]:
            clear_screen()

            print(f"You have ${player_items['money']}.")
            print("Press \"x\" to exit.")

            # Print out every available item
            print("\nAvailable Items:")
            for i in range(len(self.items)):
                item = self.items[i]
                if item[supply] > 0:
                    print(f"\t{str(i + 1)}) {item[name]} - ${str(item[cost])}")

            # Exit if the player inputs "x"
            if str(choice).upper() == "X":
                clear_screen()
                print("You have exited the shop.")
                enter_to_continue()
                return "X"

            # A little shortcut so that stuff doesn't have to be typed twice
            if choice != None:
                print(f"\n\"{choice}\" isn't an option.")

            # Get the player's choice
            choice = input("\nWhat would you like to buy?\n> ")
        return choice

    def _get_amount(self, chosen_item):
        """Get, evaluate, and format how many items the player wants"""
        
        # The following adds a little readability when accessing items
        name = 0
        cost = 1
        supply = 2

        while True:
            clear_screen()
            try:
                # Notify what the player chose
                print(f"You chose {chosen_item[name]}.")
                # Get the player's input
                amount = input("How many would you like to buy?\nType \"back\" to return to the previous menu.\n> ")
                # If the player wishes to go back, return a flag
                if amount.upper() == "BACK":
                    return amount.upper()
                # After parsing the input, try to convert it to an integer
                amount = int(amount)

                # If the player asked for a negative amount of items
                if amount < 0:
                    print("\nI'm not selling anything... yet.")
                    enter_to_continue()
                    continue

                # Loop again if the player asked for too much
                if amount > chosen_item[supply]:
                    print("\nThere isn't enough in stock.")
                    enter_to_continue()
                    continue

                break
            except ValueError:
                # The player probably inputted a non-integer
                #
                print("Enter a whole number.")
                enter_to_continue()
                continue
        return amount

    def buy(self):
        # I used a while loop so that the program can return to the beginning
        # Note to self: Recursion might be better... look into it
        while True:
            # The following adds a little readability when accessing items
            name = 0
            cost = 1
            supply = 2

            # Ask for the player's choice. If the player's input doesn't match with any options, continue asking.
            choice = self._get_choice(None)
            # If player wants to exit...
            if choice == "X":
                return
            # After getting the player's choice, store the chosen item in a variable for easier reference
            chosen_item = self.items[int(choice) - 1]

            # Get how many items the player wants
            amount = self._get_amount(chosen_item)
            # If the player inputted to return back...
            if amount == "BACK":
                continue

            total_price = (chosen_item[cost] * amount)

            # Check if the player can afford the transaction
            # If so, bill the player, subtract the item's supply and give it to the player, and print the transaction
            # If not, return to the beginning
            if total_price <= player_items['money']:
                player_items['money'] -= total_price
                chosen_item[supply] -= amount
                update_player_item(chosen_item[name], amount)
                
                print(f"\nYou bought {chosen_item[name]} x{amount} for ${total_price}.")
                print(f"\nYou now have {chosen_item[name]} x{player_items[chosen_item[name]]} and ${player_items['money']}.")
                
            else:
                print("\nYou don't have enough money.")
                enter_to_continue()
                continue

            # Note: Again, look into recursion...
            break
