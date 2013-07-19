# Takes a save.txt file as argument despite not actually having any
# save functionality (yet). '##' represents methods I am yet to code
# but will be added soon.
###############################################################################
from sys import argv

script, save_game  = argv

class ScrabbleSquare(object):
	def __init__(self, x_coord, y_coord, direction, word, board):
		# ord() converts x_coord to ASCII value and subtracts 97 so that 
		# column A has index 0, column B has index 1 etc.
		self.x = ord(x_coord) - 97
		# subtracts one so that row 1 has index 0, row 2 has index 1 etc.
		self.y = int(y_coord) - 1
		self.direction = direction
		# list() creates an array where each element is a letter of word.
		self.word = list(word)
		self.board = board
	# is_empty method checks if square with coordinates (x_coord, y_coord) 
	# has a letter placed already.
	def is_empty(self, x, y):
		# Coordinates appear to swap below as 2D lists require row selection 
		# followed by column selection (which is a little counter-intuitive).
		if self.board[y][x] == ' ':
			return True
		else:
			return False
	
	def is_valid(self):
		letter_num = 0
		# One of two different but similar loops runs depending on whether
		# word placement is horizontal(h) or vertical (v). The only difference
		# in the loops is whether letter_num tracks in a vertical or horizontal
		# direction on the board.
		if self.direction == "v":
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
				
		
	def print_word(self):
		x_axis = ['  ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
				  'I', 'J', 'K', 'L', 'M', 'N', 'O', '']
		# Print statements below print the list above separated by the string
		# that prefixes .join() below to create the x axis of the board.
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
			
		
num_tiles = 40
player = ['one', 'two']
player_num = 0
# board is initialised as a 2D list containing only single spaces. 
# It represents a blank board but spaces were used instead of 
# empty strings for ease of printing a correctly aligned board.
board = [
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
	[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],
]
	
# This Loops over the number of tiles remaining in the 'bag'.
# This loop controls the turn based element of the game.
# When we run out of tiles we end the game.
while num_tiles > 0:
	print '\nPlayer %s\'s turn...\n' % player[player_num]
	print "Enter coordinates of first letter of your word:\n"
	
	x_coord = raw_input('Enter x coordinate:\n>')
	y_coord = raw_input('Enter y coordinate:\n>')
	direction = raw_input("Enter direction of word as v(vertical) or h(horizontal):\n>")
	word = raw_input('Enter word:\n>')
	
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
		
	else:
		print "\nThe placement of this word is not valid.\n"			

	# print_word prints the updated game board to screen
	square.print_word()