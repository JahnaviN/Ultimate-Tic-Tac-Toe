class Player26:
 	def __init__(self):
		self.mov = ()

	def valueFunc(self,x,o):
		if x == 3:
			return 100
		elif o == 3:
			return -100
		elif x == 2 and o == 0:
			return 10
		elif o == 2 and x == 0:
			return -10
		elif x == 1 and o == 0:
			return 1
		elif x == 0 and o == 1:
			return -1
		else :
			return 0

	## expected utility for given state
	def computeCell(self,x,y,temp_board):
		x0 = 3*(x/3);
		y0 = 3*(y/3);
		value = 0;
		
		#diagonal
		xCount = 0 
		yCount = 0;
		i = x0; j = y0 + 2;
		for test in xrange(1,4):
			if temp_board[i][j] == 'x' :
				xCount = xCount + 1;
			elif temp_board[i][j] == 'o':
				yCount = yCount + 1;
			i = i + 1;
			j = j - 1;
		value += self.valueFunc(xCount,yCount);
		
		xCount = 0
		yCount = 0;
		i = x0 + 2; j = y0;
		for test in xrange(1,4):
			if temp_board[i][j] == 'x' :
				xCount += 1;
			elif temp_board[i][j] == 'o':
				yCount += 1;
			i = i - 1;
			j = j + 1;
		value += self.valueFunc(xCount,yCount);

		#rows
		for row in xrange(x0,x0+3):
			xCount = 0
			yCount = 0
			for col in xrange(y0,y0+3):
				if temp_board[row][col] == 'x':
					xCount += 1;
				elif temp_board[row][col] == 'o':
					yCount += 1;
			value += self.valueFunc(xCount,yCount);

		#columns
		for col in xrange(y0,y0+3):
			xCount = 0
			yCount = 0
			for row in xrange(x0,x0+3):
				if temp_board[row][col] == 'x':
					xCount += 1;
				elif temp_board[row][col] == 'o':
					yCount += 1;
			value += self.valueFunc(xCount,yCount);

		return value;

	def computeBlock(self,blockstat):
		value = 0;

		#rows
		i = 0
		for k in xrange(1,4):
			xCount = 0
			yCount = 0
			for j in xrange(1,4):
				if blockstat[i] == 'x' :
					xCount += 1
				elif blockstat[i] == 'o' :
					yCount += 1
				i += 1
			value += self.valueFunc(xCount,yCount);

		#columns	
		for i in xrange(0,3):
			k = i
			xCount = 0
			yCount = 0
			for j in xrange(1,4):
				if blockstat[k] == 'x' :
					xCount += 1
				elif blockstat[k] == 'o' :
					yCount += 1
				k += 3
			value += self.valueFunc(xCount,yCount)

		# diagonal 0-4-8
		i = 0;xCount = 0;yCount = 0
		for k in xrange(1,4):
			if blockstat[i] == 'x':
				xCount += 1
			elif blockstat[i] == 'o':
				yCount += 1
			i += 4
		value += self.valueFunc(xCount,yCount)

		# diagonal 2-4-6
		i = 2;xCount = 0;yCount = 0
		for k in xrange(1,4):
			if blockstat[i] == 'x':
				xCount += 1
			elif blockstat[i] == 'o':
				yCount += 1
			i += 2
		value += self.valueFunc(xCount,yCount)

		return value;


	def move(self,temp_board,temp_block,old_move,flag):
		#test
		#print "player 3 made a move"
		depth = 4
		alpha = -10000
		beta = 10000
		v = self.minimax(temp_board,temp_block,old_move,flag,depth,alpha,beta)
		if self.mov == ():
			print "error in minimax"
		return self.mov

	def minimax(self,board,block,old_move,flag,depth,alpha,beta):
		if depth == 0:
			#print "depth is 0"
			return self.computeCell(old_move[0],old_move[1],board) + self.computeBlock(block);

		cells = self.getCells(board,block,old_move,flag);
		
		if len(cells) == 0:
			#print "terminal nodes"
			return (self.computeCell(old_move[0],old_move[1],board) + self.computeBlock(block));
		
		if flag == 'x' :
			for c in cells:

				temp_block = []
				for i in xrange(0,9):
					temp_block.append(block[i])
				temp_board = []
				for i in xrange(0,9):
					row = []
					for j in xrange(0,9):
						row.append(board[i][j])
					temp_board.append(row)

				update_lists(temp_board,temp_block,c,flag)
				temp = alpha
				alpha = max(self.minimax(temp_board,temp_block,c,'o',depth - 1,alpha,beta),alpha)

				if depth == 4:
					if cells[0] == c:
						self.mov = c
					if temp != alpha :
						self.mov = c
				if beta <= alpha :
					break
			return alpha

		elif flag == 'o' :
			for c in cells:
				temp_block = []
				for i in xrange(0,9):
					temp_block.append(block[i])
				temp_board = []
				for i in xrange(0,9):
					row = []
					for j in xrange(0,9):
						row.append(board[i][j])
					temp_board.append(row)

				update_lists(temp_board,temp_block,c,flag)
				temp = beta;
				beta = min(self.minimax(temp_board,temp_block,c,'x',depth - 1,alpha,beta),beta)

				if depth == 4 :
					if cells[0] == c:
						self.mov = c
					if temp != beta :
						self.mov = c

				if beta <= alpha :
					break
			return beta


	def getCells(self,temp_board,temp_block,old_move,flag):

		for_corner = [0,2,3,5,6,8]

		#List of permitted blocks, based on old move.
		blocks_allowed  = []

		if old_move[0] in for_corner and old_move[1] in for_corner:
			## we will have 3 representative blocks, to choose from

			if old_move[0] % 3 == 0 and old_move[1] % 3 == 0:
				## top left 3 blocks are allowed
				blocks_allowed = [0, 1, 3]
			elif old_move[0] % 3 == 0 and old_move[1] in [2, 5, 8]:
				## top right 3 blocks are allowed
				blocks_allowed = [1,2,5]
			elif old_move[0] in [2,5, 8] and old_move[1] % 3 == 0:
				## bottom left 3 blocks are allowed
				blocks_allowed  = [3,6,7]
			elif old_move[0] in [2,5,8] and old_move[1] in [2,5,8]:
				### bottom right 3 blocks are allowed
				blocks_allowed = [5,7,8]
			else:
				print "SOMETHING REALLY WEIRD HAPPENED!"
				sys.exit(1)
		else:
		#### we will have only 1 block to choose from (or maybe NONE of them, which calls for a free move)
			if old_move[0] % 3 == 0 and old_move[1] in [1,4,7]:
				## upper-center block
				blocks_allowed = [1]
	
			elif old_move[0] in [1,4,7] and old_move[1] % 3 == 0:
				## middle-left block
				blocks_allowed = [3]
		
			elif old_move[0] in [2,5,8] and old_move[1] in [1,4,7]:
				## lower-center block
				blocks_allowed = [7]

			elif old_move[0] in [1,4,7] and old_move[1] in [2,5,8]:
				## middle-right block
				blocks_allowed = [5]
			elif old_move[0] in [1,4,7] and old_move[1] in [1,4,7]:
				blocks_allowed = [4]

                for i in reversed(blocks_allowed):
                    if temp_block[i] != '-':
                        blocks_allowed.remove(i)
	# We get all the empty cells in allowed blocks. If they're all full, we get all the empty cells in the entire board.
		cells = get_empty_out_of(temp_board, blocks_allowed,temp_block)
		return cells
