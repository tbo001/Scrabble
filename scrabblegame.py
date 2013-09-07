# Takes a save.txt file as argument despite not actually having any
# save functionality (yet). '##' represents methods I am yet to code
# but will be added soon.
###############################################################################
import argparse
import pickle
import enchant
import random


def load_game(load):
    if load:
        with open('%s.pkl' % load, 'rb') as game_load:
            board, bag, rack, player_num, players = pickle.load(game_load)
    else:
        # board is initialised as a 2D list containing only single spaces.
        # It represents a blank board but spaces were used instead of
        # empty strings for ease of printing a correctly aligned board.
        board = [[' '] * 15 for line in range(15)]

        bag = {'a': {'quantity': 8, 'value': 1},
               'b': {'quantity': 3, 'value': 3},
               'c': {'quantity': 2, 'value': 3}
               }
        players = [1, 2]
        player_num = 0
        rack = [[None] * 7 for player in players]

    return board, bag, rack, player_num, players


def print_board(board):
    x_axis = ['  ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
              'I', 'J', 'K', 'L', 'M', 'N', 'O', '']
    # Print statements below print the list above separated by the string
    # that prefixes .join() below to create the x axis of the board
    # The second print statement print a line of dashes to separate the
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


def save_game(load, save, board, bag, rack, player_num, players):
    if load:
        with open('%s.pkl' % load, 'wb') as game_save:
            pickle.dump((board, bag, rack, player_num, players), game_save)
    else:
        with open('%s.pkl' % save, 'wb') as game_save:
            pickle.dump((board, bag, rack, player_num, players), game_save)


def print_rack(rack, player_num):
    # print 'Your rack:', ' '.join(rack[player_num]), '\n'
    tile_num = 0
    for tile in rack[player_num]:
        if tile:
            print tile,
        else:
            print '',
    print '\n'


def get_letters(rack, bag, player_num):
    letter = LetterBag(bag)
    tile_num = 0
    for tile in rack[player_num]:
        if tile is None:
            rack[player_num][tile_num] = letter.choose()
            print rack
            if rack[player_num][tile_num]:
                letter.take()
        tile_num += 1


def a_rack_is_empty(rack, players):
    for player in players:
        if rack[player - 1] == [None] * 7:
            return True
        else:
            return False


class LetterBag(object):
    def __init__(self, bag):
        self.bag = bag

    def choose(self):
        if self.bag:
            self.letter = random.choice(self.bag.keys())
            return self.letter
        else:
            print 'The bag is empty!'
            return None

    def value(self):
        return self.bag[self.letter]['value']

    def quantity(self):
        return self.bag[self.letter]['quantity']

    def take(self):
        self.bag[self.letter]['quantity'] -= 1
        if not self.bag[self.letter]['quantity']:
            del self.bag[self.letter]

        print self.bag  # DIAGNOSTIC


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
    def is_word(self, word):
        dictionary = enchant.Dict("en_GB")
        print "Word is", word  # DIAGNOSTIC
        return dictionary.check(word)

    def is_empty(self, x, y):
        # Coordinates appear to swap below as 2D lists require row selection
        # followed by column selection (which is a little counter-intuitive).
        if (x > 14) or (y > 14):
            return True
        else:
            return self.board[y][x] == ' '

    def letter_placement_valid(self, x, y, letter):
    # Nested ifs below first check if square is non-empty and,
    # if so, then checks if the letter to be played is different
    # from the letter already occupying that square on the board.
        if not self.is_empty(x, y) and letter != self.board[y][x]:
            return False
        else:
            return True

    def placement_is_valid(self):
        letter_num = 0
        # One of two different but similar loops runs depending on whether
        # word placement is horizontal(h) or vertical (v). The only difference
        # in the loops is whether letter_num tracks in a vertical or horizontal
        # direction on the board.
        # self.is_valid_direction(self. x, self.y)
        if self.direction == "v":
            for letter in self.word:
                if not self.letter_placement_valid(self.x, self.y + letter_num, letter):
                    return False
                letter_num += 1
                # letter_num is a counting variable which allows us to track
                # how far we have moved from the tile containing the first
                # letter of our played word.
            # If the loop runs through each letter in word without returning
            # False then the placement of the word is valid and True is
            # returned.
            return True

        else:
            for letter in self.word:
                if not self.letter_placement_valid(self.x + letter_num, self.y, letter):
                    return False
                letter_num += 1
            return True

    def parallel_word_valid(self):
        square_pre_dist = 0
        square_post_dist = len(self.word)
        if self.direction == 'v':
            while not self.is_empty(self.x, self.y + (square_pre_dist - 1)):
                square_pre_dist -= 1

            while not self.is_empty(self.x, self.y + square_post_dist):
                square_post_dist += 1

            parallel_word = [self.board[self.y + i][self.x] for i in range(square_pre_dist, 0)]
            parallel_word.append(self.word)
            parallel_word.append(''.join(self.board[self.y + i][self.x]
                                         for i in range(len(self.word), square_post_dist)))
            parallel_word = ''.join(parallel_word)
        else:
            while not self.is_empty(self.x + (square_pre_dist - 1), self.y):
                square_pre_dist -= 1

            while not self.is_empty(self.x + square_post_dist, self.y):
                square_post_dist += 1

            parallel_word = [self.board[self.y][self.x + i] for i in range(square_pre_dist, 0)]
            parallel_word.append(self.word)
            parallel_word.append(''.join(self.board[self.y][self.x + i]
                                         for i in range(len(self.word), square_post_dist)))
            parallel_word = ''.join(parallel_word)
        print square_pre_dist, square_post_dist  # DIAGNOSTIC
        print "Parallel word is: ", parallel_word
        return self.is_word(parallel_word)

    def adjacent_words_valid(self):
        return self.parallel_word_valid() # and perpendicular_words_valid()

    def is_valid(self):
        return self.placement_is_valid() and self.adjacent_words_valid()

    def place_letter(self, letter, rack, player_num):
        tile_num = 0
        matches = 0
        for tile in rack[player_num]:
            if (tile == letter) and (matches == 0):
                rack[player_num][tile_num] = None
                matches += 1
            tile_num += 1

    def place_word(self, rack, player_num):
        letter_num = 0
        if self.direction == "v":
            for letter in self.word:
                self.board[self.y + letter_num][self.x] = letter
                self.place_letter(letter, rack, player_num)
                letter_num += 1
        else:
            for letter in self.word:
                self.board[self.y][self.x + letter_num] = letter
                self.place_letter(letter, rack, player_num)
                letter_num += 1


def main():
    parser = argparse.ArgumentParser(description='Start a scrabble game!')
    parser.add_argument('save_name', nargs='?', default='save')
    parser.add_argument('--load', nargs='?', const='save', default=0)

    args = parser.parse_args()

    board, bag, rack, player_num, players = load_game(args.load)

    # This Loops over the number of tiles remaining in the 'bag'.
    # This loop controls the turn based element of the game.
    # When we run out of tiles we end the game.
    while bag or not a_rack_is_empty(rack, players):
        # print_board prints the updated game board to screen
        print_board(board)
        get_letters(rack, bag, player_num)
        print '\nPlayer %s\'s turn...\n' % players[player_num]
        print_rack(rack, player_num)
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
            square.place_word(rack, player_num)

            # score counts the points attained by the played word
            ##square.score()##

            # player_num is the index position of the list 'player'.
            # It adds one after each turn so that the next player can be alerted
            # if it is their turn by a statement printed to the screen.
            # It is mod 2 because (currently) this game is for only two players.
            # Additional input can easily be accepted later to allow for more than
            # two players.
            player_num = (player_num + 1) % 2

            save_game(args.load, args.save_name, board, bag, rack, player_num, players)

        else:
            print "\nThe placement of this word is not valid.\n"

if __name__ == '__main__':
    main()
