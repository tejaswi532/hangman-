import curses
import random 
import string

DASH = "-"
alphabets = "abcdefghijklmnopqrstuvwxyz"

positions = {"HEAD_Y" : 4, "HEAD_X" : 35, "NECK_Y" : 5, "NECK_X" : 35, "BODY_Y" : 6, "BODY_X" : 35, "RIG_HAND_Y" : 5, "RIG_HAND_X" : 34, "LEFT_HAND_Y" : 5, "LEFT_HAND_X" : 36, "RIG_LEG_Y" : 7, "RIG_LEG_X" : 34, "LEFT_LEG_Y" : 7, "LEFT_LEG_X" : 36}

while True:
    used = []
    def choose_word():
        lines = [word.strip() for word in open("words.txt")]
        return random.choice(lines)

    def updating_dashes(chosen_letter, dashes, letter_list):
        chosen_letter_count = 0
        for index, character in enumerate(letter_list):
            if chosen_letter == character:
                chosen_letter_count  += 1
                dashes[index] = character
        return(chosen_letter_count, ''.join(dashes))

    stdscr = curses.initscr()

    def draw_hangman(chances_left):
        if chances_left == 6:
            stdscr.addstr(positions["HEAD_Y"], positions["HEAD_X"], "O")
        elif chances_left == 5:
            stdscr.addstr(positions["NECK_Y"], positions["NECK_X"], "|")
        elif chances_left == 4:
            stdscr.addstr(positions["RIG_HAND_Y"], positions["RIG_HAND_X"], "/")
        elif chances_left == 3:
            stdscr.addstr(positions["LEFT_HAND_Y"], positions["LEFT_HAND_X"], "\\")
        elif chances_left == 2:
            stdscr.addstr(positions["BODY_Y"], positions["BODY_X"], "|")
        elif chances_left == 1:
            stdscr.addstr(positions["RIG_LEG_Y"], positions["RIG_LEG_X"], "/")
        else:
            stdscr.addstr(positions["LEFT_LEG_Y"], positions["LEFT_LEG_X"], "\\")

    def guess_letter(input_position):
        stdscr.addstr(18, 16, "letters typed : ")
        while True:
            key_entered = stdscr.getstr(18, input_position, 1).decode('utf-8').lower()
            #stdscr.addstr(22, 20, "=>>> " + key_entered + " <<<==")
            input_position += 1
            if key_entered not in alphabets:
                stdscr.addstr(20, 16, "Select an Alphabet.                       ")
            elif key_entered in used:
                stdscr.addstr(20, 16, "Letter already used, Please try again!")
            else:
                used.append(key_entered)
                return key_entered

    def game(dashes, letter_list):
        letters_found = 0
        chances_left = 7
        input_position = 32
        game_over =  False

        while not game_over:
            key_entered = guess_letter(input_position)
            input_position += 1

            chosen_letter_count, updated_dashes = updating_dashes(key_entered, dashes, letter_list)
            letters_found  += chosen_letter_count

            if letters_found == len(letter_list):
                stdscr.addstr(20, 16, "'CONGRATULATIONS!,You won the game'     ")
                game_over = True

            if chosen_letter_count != 0:
                stdscr.addstr(16, 23, updated_dashes)
                stdscr.addstr(20, 16, "Correct guess                                ")
            else:
                chances_left -= 1
                stdscr.addstr(20, 16, "letter not in the word, try again          ")
                draw_hangman(chances_left)

                if chances_left == 0:
                    stdscr.addstr(20, 16, "your chances are over,You lost           ")
                    stdscr.addstr(21, 16, ''.join(letter_list))
                    game_over = True

    def display(dashes):
        for x in range(20, 36):
            stdscr.addstr(2, x, "_")
        for x in range(3, 10):
            stdscr.addstr(x, 19, "|")

        stdscr.addstr(3, 35, "|")

        for x in range(12, 32):
            stdscr.addstr(10, x, "_")
        for x in range(11, 14):
            stdscr.addstr(x, 11, "|")
        for x in range(12, 40):
            stdscr.addstr(13, x, "_")

        stdscr.addstr(11, 32, "|")

        for x in range(33, 40):
            stdscr.addstr(11, x, "_")
        for x in range(12, 14):
            stdscr.addstr(x, 40, "|")

        stdscr.addstr(16, 16, "Word : ")    
        stdscr.addstr(16, 23, ''.join(dashes))

    letter_list = list(choose_word())
    dashes = list(DASH * len(letter_list))
    display(dashes)
    game(dashes, letter_list)

    stdscr.addstr(22, 16, "Do you want to play again?? (y / n)")
    play_again_choice = stdscr.getstr(22, 55, 1).decode('utf-8').lower()
    curses.curs_set(0)

    while play_again_choice != 'n' and play_again_choice != 'y':
        stdscr.addstr(22, 16, "Enter either y or n                  ")
        play_again_choice = stdscr.getstr(22, 55, 1).decode('utf-8').lower()

    if play_again_choice == 'n':
        break

    stdscr.clear()

    curses.endwin()




