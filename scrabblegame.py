# Takes a save.txt file as argument despite not actually having any
# save functionality (yet). '##' represents methods I am yet to code
# but will be added soon.
###############################################################################
import argparse
import pickle
import enchant


def load_game(load):
    if load:
        with open('%s.pkl' % load, 'rb') as game_load:
            board = pickle.load(game_load)
    else:
        # board is initialised as a 2D list containing only single spaces.
        # It represents a blank board but spaces were used instead of
        # empty strings for ease of printing a correctly aligned board.
        board = [[' '] * 15 for line in range(15)]
    return board


def print_board(board):
    x_axis = ['  ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
              'I', 'J', 'K', 'L', 'M', 'N', 'O', '']
    # Print statements below print the list above separated by the string
    # that prefixes .join() below to create the x axis of the board# The second print statement print a line of dashes to separate the
    # axis from the next line of the game board.
    print '\n'
    print ' | '.join(x_axis)
    print '- ' * 32
    line_num = 1
    # The for loop below loops over each row in the game board and prints
    # the row number followed by the the corresponding row of the gameboard
    # with each square separated by a '|' character.
    for line in board:
        # When line_num is >= 10 we need one less space before the '|' to
        # ensure the board correctly lines up when printed (as anything 10
        # or greater is a 2 digit number instead of single digit)
        if line_num < 10:
            print '%d  |' % line_num, ' | '.join(line), '|'
        else:
            print '%d |' % line_num, ' | '.join(line), '|'
        print '- ' * 32
        line_num += 1


def get_input(prompt, error, input_type):
    input = -1
    while not input_is_true(input, input_type):
        input = raw_input(prompt)
        if not input_is_true(input, input_type):
            print error
    return input


def input_is_true(input, input_type):
    x_axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h','i', 'j', 'k', 'l', 'm', 'n', 'o']
    y_axis = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']

    if (input_type == 'x_coordinate') and (input in x_axis):
        return True
    elif (input_type == 'y_coordinate') and (input in y_axis):
        return True
    elif (input_type == 'direction') and (input in ['v', 'h']):
        return True
    elif input_type == 'word':
        dictionary = enchant.Dict("en_GB")
        if dictionary.check(input):
            return True
        else:
            return False
    else:
        return False


def save_game(load, save, board):
    if load:
        with open('%s.pkl' % load, 'wb') as game_save:
            pickle.dump(board, game_save)   
    else:
        with open('%s.pkl' % save, 'wb') as game_save:
            pickle.dump(board, game_save)


class ScrabbleSquare(object):
    def __init__(self, x_coord, y_coord, direction, word, board):
        # ord() converts x_coord to ASCII value and subtracts 97 so that
        # column A has index 0, column B has index 1 etc.
        self.x = ord(x_coord) - 97
        # subtracts one so that row 1 has index 0, row 2 has index 1 etc.
        self.y = int(y_coord) - 1
        self.direction = direction
        self.word = word
        self.board = board

    # is_empty method checks if square with coordinates (x_coord, y_coord)
    # has a letter placed already.
    def is_empty(self, x, y):
        # Coordinates appear to swap below as 2D lists require row selection
        # followed by column selection (which is a little counter-intuitive).
        return self.board[y][x] == ' '

    def is_valid(self):
        letter_num = 0
        # One of two different but similar loops runs depending on whether
        # word placement is horizontal(h) or vertical (v). The only difference
        # in the loops is whether letter_num tracks in a vertical or horizontal
        # direction on the board.
        if self.direction == "v":
            #self.is_valid_direction(self. x, self.y)
            for letter in self.word:
                # Nested ifs below first check if square is non-empty and,
                # if so, then checks if the letter to be played is different
                # from the letter already occupying that square on the board.
                if not self.is_empty(self.x, self.y + letter_num):
                    if letter != self.board[self.y + letter_num][self.x]:
                        return False
                # letter_num is a counting variable which allows us to track
                # how far we have moved from the tile containing the first
                # letter of our played word.
                letter_num += 1
            # If the loop runs through each letter in word without returning
            # False then the placement of the word is valid and True is
            # returned.
            return True

        else:
            for letter in self.word:
                if not self.is_empty(self.x + letter_num, self.y):
                    if letter != self.board[self.y][self.x + letter_num]:
                        return False
                letter_num += 1
            return True

    def place_word(self):
        letter_num = 0
        if self.direction == "v":
            for letter in self.word:
                self.board[self.y + letter_num][self.x] = letter
                letter_num += 1
        else:
            for letter in self.word:
                self.board[self.y][self.x + letter_num] = letter
                letter_num += 1


def main():
    parser = argparse.ArgumentParser(description='Start a scrabble game!')
    parser.add_argument('save_name', nargs='?', default='save')
    parser.add_argument('--load', nargs='?', const='save', default=0)

    args = parser.parse_args()

    board = load_game(args.load)

    num_tiles = 40
    player = ['one', 'two']
    player_num = 0

    # This Loops over the number of tiles remaining in the 'bag'.
    # This loop controls the turn based element of the game.
    # When we run out of tiles we end the game.
    while num_tiles > 0:
        # print_board prints the updated game board to screen
        print_board(board)
        print '\nPlayer %s\'s turn...\n' % player[player_num]
        print "Enter coordinates of first letter of your word:\n"

        x_coord = get_input('Enter x coordinate:\n>',
                            'x_coordinate must be a letter from a to o!\n',
                            'x_coordinate')
        y_coord = get_input('Enter y coordinate:\n>',
                            'y coordinate must be a number from 1 to 15!\n',
                            'y_coordinate')
        direction = get_input("Enter direction of word as v(vertical) or h(horizontal):\n>",
                              'Direction must be either \'h\' or \'v\'!\n',
                              'direction')
        word = get_input('Enter word:\n>',
                         'Not a valid English word!\n',
                         'word')

        square = ScrabbleSquare(x_coord, y_coord, direction, word, board)

        # is_valid method checks if  the letters in 'word' contradict any letters
        # already placed in the squares 'word' falls on
        if square.is_valid():
        ##square.is_word()## # This method will check if the played word is
        # in the dictionary
            # place_word places the new word in the correct position in the
            # list 'board'.
            square.place_word()

            # score counts the points attained by the played word
            ##square.score()##

            # player_num is the index position of the list 'player'.
            # It adds one after each turn so that the next player can be alerted
            # if it is their turn by a statement printed to the screen.
            # It is mod 2 because (currently) this game is for only two players.
            # Additional input can easily be accepted later to allow for more than
            # two players.
            player_num = (player_num + 1) % 2

            save_game(args.load, args.save_name, board)

        else:
            print "\nThe placement of this word is not valid.\n"

if __name__ == '__main__':
    main()
