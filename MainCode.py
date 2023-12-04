import random
import os
import time
import math
from rich.console import Console
from rich.progress import track
from tqdm import tqdm

console = Console()

#################################### AESTHETIC FUNCTIONS ####################################
# Functions for printing in color
def print_red(text, end="\n"):
    print("\033[31m {}\033[00m".format(text), end=end)

def print_orange(text, end="\n"):
    print("\033[33m {}\033[00m".format(text), end=end)

def print_blue(text, end="\n"):
    print("\033[34m {}\033[00m".format(text), end=end)

def print_purple(text, end="\n"):
    print("\033[35m {}\033[00m".format(text), end=end)

def print_green(text, end="\n"):
    print("\033[32m {}\033[00m".format(text), end=end)


# Function to clear the terminal
def clear_terminal():
    os.system("clear")

# Function to print a colored piece without a newline
def print_colored_tile(text, color):
    if color == "Red":
        print_red(text, end="")
        return
    if color == "Purple":
        print_purple(text, end="")
        return
    if color == "Blue":
        print_blue(text, end="")
        return
    if color == "Orange":
        print_orange(text, end="")
        return
    if color == "Green":
        print_green(text,end="")
        return
    print(text, end="")

    # Welcome to the game
def welcome():
    clear_terminal()
    console.print(
          "____                                    _   _  __          _      \n"
        + "  |  _ \   _   _   _ __ ___    _ __ ___   (_) | |/ /  _   _  | |__ \n"
        + "   | |_) | | | | | | '_ ` _ \  | '_ ` _ \  | | | ' /  | | | | | '_ \ \n"
        + "   |  _ <  | |_| | | | | | | | | | | | | | | | | . \  | |_| | | |_) |\n"
        + "   |_| \_\  \__,_| |_| |_| |_| |_| |_| |_| |_| |_|\_\  \__,_| |_.__/ \n",justify="center",style="bold",
    )

    # Print a welcome message with emoji and styling
    print("\n\n")
    console.print("\n\n:fire: Rummikub from UoN :fire:", justify="center", style="bold cyan")


def progressBar():
    for _ in tqdm(range(100), desc="Loading......."):
        time.sleep(0.05)


# Function to start the game
def startGameTxt():
    clear_terminal()
    console.print("\n\n Lets Go!", justify="center")
    console.print("May the best Player 'Win' ", justify="center")
    time.sleep(1.5)

# Function to end the game
def final_game(player):
    clear_terminal()

    console.print("The game has ended! You ran out of tiles!", justify="center")
    console.print("THE WINNER IS:\n", justify="center")
    console.print(f"\tPlayer {player + 1}\n", justify="center")

    console.print(
        " _          _  _                               \n"
        +"\ \      / / ( )  _ __    _ __     _ _   _ __ \n"
        +" \ \ /\ / /  | | | '_ \  | '_ \   / _ \ | '__| \n"
        +"  \ V  V /   | | | | | | | | | | |  __/ | |   \n"
        +"   \/  \/    | | | | | | | | | |  \__|  | |   ",justify="center"
    )

#################################### GAME FUNCTIONS ####################################
# Function to print the current state of the game on the screen
def show_game_state(player_number, player_hand):
    console.print(f"PLAYER {player_number + 1}", style="bold")
    print("\n\t■ The current board is: ")
    show_board(board)
    print("\n\t■ Your hand:")
    show_hand(player_hand)

    # Show the available actions
    print("\n\t■ Available actions:")
    show_turn(can_pass, can_draw_tile)



# Function to create the tiles to be used in the game
def create_tiles(num_decks=1):
    tiles = []

    colors = ["Orange", "Blue", "Purple", "Red", "Green"]

    for _ in range(num_decks):
        for color in colors:
            for value in range(1, 16):
                tile_value = "{} {}".format(color, value)
                tiles.append(tile_value)

    return tiles

def verify_deck_repetitions(deck, max_repetitions, num_decks):
    tile_count = {}
    for tile in deck:
        tile_count[tile] = tile_count.get(tile, 0) + 1
        if tile_count[tile] > max_repetitions * num_decks:
            return False
    return True

def show_deck(deck):
    if not deck:
        print("The deck is empty.")
        return
    print("Current Deck:")
    for tile in deck:
        print(tile, end=", ")
    print("\n")


# Function to shuffle tiles
import random
def shuffle_tiles(tiles):
    random.shuffle(tiles)
    return tiles

def draw_starting_tiles(players, rummikub_tiles):
    starting_numbers = []

    # Each player draws a tile
    for player_index in range(len(players)):
        starting_tile = rummikub_tiles.pop(0)
        players[player_index].append(starting_tile)

        split_tile = starting_tile.split(" ")
        tile_value = int(split_tile[1])
        starting_numbers.append((player_index, tile_value))

        console.print(
            f"Player {player_index + 1} drew tile: {starting_tile}", style="italic"
        )

    # Sort players based on the drawn tile values
    starting_numbers.sort(key=lambda x: x[1], reverse=True)

    console.print("\nPlayers' drawn tiles and values:")
    for player_index, tile_value in starting_numbers:
        console.print(f"Player {player_index + 1}: {tile_value}", style="italic")

    starting_player = starting_numbers[0][0]
    console.print(f"\nPlayer {starting_player + 1} starts first!", style="bold")

    # Put drawn tiles back to the deck
    for player_index, _ in starting_numbers:
        rummikub_tiles.extend(players[player_index])

    # Shuffle the tiles again
    rummikub_tiles = shuffle_tiles(rummikub_tiles)

    return starting_player

# Function to pick tiles
def pick_tiles(num_tiles):
    player_tiles = []
    for _ in range(num_tiles):
        player_tiles.append(rummikub_tiles.pop(0))
    return player_tiles

# Function to display the current player's hand
def show_hand(player_hand):
    print("|" + "-" * 120 + "|")
    per_row = 7
    count = 1
    for row in range(math.ceil(len(player_hand) / per_row)):
        for col in range(per_row):
            if count > len(player_hand):
                break
            split_tile = player_hand[col + (row * per_row)].split(" ", 1)
            color = split_tile[0]
            print(f"({count})", end="")
            print_colored_tile(f"{player_hand[col + (row * per_row)]}\t", color)
            count += 1
        print("")
    print("|" + "-" * 120 + "|")

def show_turn(can_pass,can_draw_tile):
    if can_draw_tile:
        console.print(
            "[bold cyan]Option 1:[/bold cyan] [underline]Pick a tile.[/underline]"
        )

    if can_pass > 1 or len(board) >= 1:
        console.print(
            "[bold cyan]Option 2:[/bold cyan] [underline]Add tile to an existing position.[/underline]"
        )

    console.print(
        "[bold cyan]Option 3:[/bold cyan] [underline]Add tile to a new position.[/underline]"
    )

    if can_pass:
        console.print(
            "[bold cyan]Option 4:[/bold cyan] [underline]Pass turn.[/underline]"
        )

# Function to display a pile of tiles on the board
def show_pile(pile):
    count = 1
    for tile in pile:
        split_tile = tile.split(" ", 1)
        color = split_tile[0]
        print_colored_tile(f"{tile}", color)
        count += 1
        if count <= len(pile):
            print(" -", end="")

# Function to display the game board
def show_board(board):
    print("|" + "-" * 120 + "|")
    per_row = 3
    number = 1
    for row in range(math.ceil(len(board) / per_row)):
        for col in range(per_row):
            if number > len(board):
                break
            print("", end="")
            print(f"({number})", end="")
            show_pile(board[col + (row * per_row)])
            print("\t\t", end="")
            number += 1
        print("")
    print("|" + "-" * 120 + "|")

# First option of the turn: Add a tile to the player's hand
# Modified option1 function
# Updated option1 function
def option1(player_hand):
    global rummikub_tiles
    global player_turn

    # Draw two tiles
    drawn_tiles = pick_tiles(2)

    # Display the drawn tiles and let the player choose one to add to the hand
    print("\nYou drew the following tiles:")
    for i, tile in enumerate(drawn_tiles, start=1):
        print(f"({i}) {tile}")

    chosen_tile_index = int(input("\nChoose a tile to add to your hand (enter the corresponding number): "))

    # Add the chosen tile to the player's hand
    chosen_tile = drawn_tiles.pop(chosen_tile_index - 1)
    player_hand.append(chosen_tile)
    print_green("\nYour chosen tile has been successfully added to your hand.")

    # Return the remaining tile to the pool
    returned_tile = drawn_tiles[0]
    rummikub_tiles.append(returned_tile)
    print_blue(f"\nThe other tile ({returned_tile}) has been returned to the pool.")

    # Increment player_turn to pass the turn to the next player
    player_turn += 1
    if player_turn == num_players:
        player_turn = 0

    time.sleep(0.8)  # Add a delay for better user experience

# Second option of the turn: Add a tile to an existing position on the board
def option2():
    global user_tile
    global board_set

    user_tile = int(input("Choose the tile you want to add: "))

    if user_tile > len(players[player_turn]):
        print_red("\tYou don't have this tile in your hand.")
        return False

    board_set = int(input("Choose the board set where you want to add it: "))
    if board_set > len(board):
        print_red("\tThis board set is not on the board.")
        return False
    elif board_set <= len(board):
        correct = rules_option_2()

        if correct:
            # Remove the tile from the player's hand
            removed_tile = players[player_turn].pop(user_tile - 1)
            print_green(f"\nYour tile {removed_tile} has been successfully added.")

        return correct

    
# Third option of the turn: Add tiles to a new position on the board
# Function to add tiles to a new position on the board
def option3(player_hand):
    global new_set
    global user_tile

    new_set = []
    finish_pile = False

    while not finish_pile:
        user_tile = int(
            input(
                "\nChoose the tile you want to add. If you don't want to add more, insert 0: "
            )
        )

        if user_tile == 0:
            if len(new_set) <= 2:
                print_red("\tThe minimum set must consist of 3 tiles.")
                cancel_option = input("Do you want to cancel the operation? (y/n)")

                if str(cancel_option).lower() == "y":
                    finish_pile = True
                    players[player_turn].extend(new_set)
                    new_set.clear()

                elif (
                    str(cancel_option).lower() != "n" or str(cancel_option).lower() != "y"
                ):
                    print_red("\tInvalid option.")

            else:
                finish_pile = True
                board.append(new_set)

        # If the number entered exceeds the hand index, it indicates that the player doesn't have the tile and closes the loop
        elif user_tile > len(players[player_turn]):
            print_red("\tYou don't have this tile in your hand.")

        else:
            # Adds the tile to the set and removes it from the hand
            if len(new_set) == 0:
                new_set.append(players[player_turn][user_tile - 1])
                players[player_turn].pop(user_tile - 1)
                print_green("\nYour tile has been successfully added.")
            else:
                if rules_option_3():
                    players[player_turn].pop(user_tile - 1)
                    print_green("\nYour tile has been successfully added.")
                else:
                    print_red("\tThis tile cannot be added to the set.")

            print("\n\n\t■ Your new hand is: ")
            show_hand(player_hand)

            print("\n\t■ The set you want to add, for now, is: ", end="")
            show_pile(new_set)

    return len(new_set) != 0

# Rules for the second option: Add a tile to an existing position on the board
# Updated rules_option_2 function
def rules_option_2():
    # Save the color and number of the selected tile
    user_tile_color = players[player_turn][user_tile - 1].split(" ")[0]
    user_tile_number = int(players[player_turn][user_tile - 1].split(" ")[1])

    # Create lists of colors and numbers of tiles on the board separately
    board_colors_list = []
    board_numbers_list = []

    # Access the tiles in the selected set on the board and separate them into color and number.
    # Then add them to the created lists
    for i in board[board_set - 1]:
        tile_color = i.split(" ")[0]
        tile_number = int(i.split(" ")[1])
        board_colors_list.append(tile_color)
        board_numbers_list.append(tile_number)

    # Check if the selected tile can be added to the existing set as a trio (same number, different colors)
    if board_numbers_list.count(user_tile_number) >= 5:
            print_red("\tYou cannot have more than 5 tiles with the same number in a set.")
            return False
    elif user_tile_number in board_numbers_list:
        # Add the tile to the existing set
        board[board_set - 1].append(players[player_turn][user_tile - 1])
        print_green("\nYour tile has been successfully added.")
        return True
    

    # Check if the selected tile can be added to the existing set as a sequence of even or odd numbers of the same color
    if (
        user_tile_color == board_colors_list[0]
        and (
            user_tile_number == (max(board_numbers_list) + 2)  # Check for even sequence
            or user_tile_number == (min(board_numbers_list) - 2)  # Check for odd sequence
        )
    ):
        # Add the tile to the existing set
        if user_tile_number == (max(board_numbers_list) + 2):
            board[board_set - 1].append(players[player_turn][user_tile - 1])
        else:
            board[board_set - 1].insert(0, players[player_turn][user_tile - 1])
        print_green("\nYour tile has been successfully added.")
        return True

    # If neither condition is met, it's an incorrect move
    print_red("\tIncorrect move, try again.")
    return False


# Function to enforce rules for the third option: Add tiles to a new position on the board
def rules_option_3():
    # Save the color and number of the selected tile
    user_tile_color = players[player_turn][user_tile - 1].split(" ")[0]
    user_tile_number = int(players[player_turn][user_tile - 1].split(" ")[1])

    # Create lists of colors and numbers of tiles in the new set being created
    new_set_colors_list = []
    new_set_numbers_list = []

    # Access the tiles in the new set on the board and separate them into color and number.
    # Then add them to the created lists
    for tile in new_set:
        tile_color = tile.split(" ")[0]
        tile_number = int(tile.split(" ")[1])
        new_set_colors_list.append(tile_color)
        new_set_numbers_list.append(tile_number)

    # Main loop for the rules.
    # Determines if the set consists of tríos or escalera de números and executes one rule or another
    if new_set_numbers_list[0] == user_tile_number:
        # RULE - TRÍOS
        correct_move = False
        while not correct_move:
            if user_tile_color in new_set_colors_list:
                print_red("\tIncorrect move, try again.")
                return False

            elif user_tile_number != new_set_numbers_list[0]:
                print_red("\tIncorrect move, try again.")
                return False

            else:
                correct_move = True
                new_set.append(players[player_turn][user_tile - 1])
                return True
    else:
        # RULE - ESCALERA
        correct_move = False
        while not correct_move:
            if (
                user_tile_color != new_set_colors_list[0]
                or user_tile_number != (new_set_numbers_list[-1] + 2)  # Check for even sequence
                and user_tile_number != (new_set_numbers_list[0] - 2)  # Check for odd sequence
            ):
                print_red("\tIncorrect move, try again.")
                return False

            elif user_tile_number == (new_set_numbers_list[0] - 2):  # Check for odd sequence
                correct_move = True
                new_set_numbers_list.append(user_tile_number)
                new_set_numbers_list.sort()
                new_set.insert(0, players[player_turn][user_tile - 1])
            else:
                correct_move = True
                new_set.append(players[player_turn][user_tile - 1])

        return correct_move


# Create the set of tiles shuffled randomly
rummikub_tiles = create_tiles(num_decks=1) # creates Deck size
rummikub_tiles = shuffle_tiles(rummikub_tiles) # Shuffling the tiles

max_repetitions_allowed = 2  # Define maximum repetitions allowed per tile
if not verify_deck_repetitions(rummikub_tiles, max_repetitions_allowed, 2):
    print_red("Error: Deck verification failed due to excessive repetitions of some tiles.")
# Create the board list
board = []

# Welcome the players
welcome()

# Define the number of players
#players = []
# Define the number of players
num_players = int(console.input("[bold]How many players?[/bold] "))
while num_players < 2 or num_players > 4:
    print_red("\tInvalid. Please insert a number between 2 and 4.\n")
    num_players = int(console.input("How many players? "))

# Initialize the players list with an empty list for each player
players = [[] for _ in range(num_players)]

# Now call the draw_starting_tiles function
starting_player = draw_starting_tiles(players, rummikub_tiles)



print("Great! Everything will be ready in a few seconds.\n")
progressBar()

# After determining the starting player, remove the initially drawn tile from each player's hand
for player_hand in players:
    player_hand.pop()

# Distribute 14 tiles to each player for the game start
for player in range(num_players):
    players[player].extend(pick_tiles(14))

#################################    
# Display the current deck
show_deck(rummikub_tiles)

# verified the count of cards in decks
total_count = len(rummikub_tiles)
print(f'Total tile count: {total_count}')
##################################
# Define the player's turn, game turn, and the condition for the main game loop using a boolean
player_turn = starting_player
#player_turn = 0
game_turn = 1
playing = True

# Define if it is the first turn
first_turn = True

# Split the value and color of the tile to make comparisons
split_tile = rummikub_tiles[0].split(" ", 1)
color = split_tile[0]
tile_value = int(split_tile[1])

# Boolean to detect if the player can pass and if they can draw a tile,
# so the options are shown or not in the menu
can_pass = False
can_draw_tile = True

startGameTxt()

# Main loop:
while playing:

    # If it's not the first turn
    if not first_turn:

        can_draw_tile = True
        can_pass = False
        finish_action = False

        while not finish_action:
            time.sleep(1)
            clear_terminal()

            # Display the player's hand and the board.
            show_game_state(player_turn, players[player_turn])

            while True:
                try:
                    action = int(input("\nWhat option do you choose?: "))
                    break
                except ValueError:
                    print_red("\tPlease enter a valid number.")

            if action == 1 and can_draw_tile:
                # Draw a tile and add it to the player's hand
                option1(players[player_turn])

            elif action == 2:
                correct = option2()

                if correct:
                    can_draw_tile = False
                    can_pass = True

            elif action == 3:
                correct = option3(players[player_turn])

                if correct:
                    can_draw_tile = False
                    can_pass = True

            elif action == 4:
                finish_action = True

            else:
                print_red("\tInvalid option")

    # If it's the first turn:
    else:
        can_draw_tile = True
        can_pass = False
        finish_action = False

        while not finish_action:
            time.sleep(1)
            clear_terminal()

            # Display the player's hand and the board.
            show_game_state(player_turn, players[player_turn])

            while True:
                try:
                    action = int(input("\nWhat option do you choose?: "))
                    break
                except ValueError:
                    print_red("\tPlease enter a valid number.")

            if action == 1 and can_draw_tile:
                # Draw a tile and add it to the player's hand
                option1(players[player_turn])

            elif action == 2:
                correct = option2()

                if correct:
                    can_pass = True

            elif action == 3:
                correct = option3(players[player_turn])

                if correct:
                    can_pass = True

            elif action == 4:
                # Split the tile and sum the numeric value
                tile_value = 0
                for tile_set in board:
                    for tile in tile_set:
                        split_tile = tile.split(" ")
                        tile_value += int(split_tile[1])

                # Check if the total value of the added tile sets is greater than or equal to 30
                if tile_value < 30:
                    print_red("\tThe total value of the added tile sets is less than 30.")
                else:
                    finish_action = True
                    if game_turn == num_players:
                        first_turn = False
            else:
                print_red("\tInvalid option \n")

    if len(players[player_turn]) == 0:  # If the player's hand is empty, the game ends
        playing = False
    else:
        # Move to the next turn
        player_turn = player_turn+ 1
        time.sleep(1.5)

        if player_turn == num_players:
            player_turn = 0

        # Increment the overall game turn by 1
        game_turn += 1

final_game(player_turn)