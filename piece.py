

class Pawn:
	def __init__(self,i,j,color):
		self.i = i
		self.j = j
		self.color = color
		
	
	def valid_moves(self,board,pins,enpassant_possible):
		valid_moves = []
		i, j = self.i, self.j
		
		piece_pinned = False
		pin_direction = ()
		if pins:
			for k in range(len(pins)-1,-1,-1):
				if pins[k][0] == i and pins[k][1] == j:
					piece_pinned = True
					pin_direction = (pins[k][2],pins[k][3])
					break 

		if self.color == 'w':
			if 0 < i :
				piece = board[i-1][j]
				if piece == '0':
					if not piece_pinned or pin_direction == (-1,0):
						if piece[0] != self.color:
							valid_moves.append([(i,j),(i-1,j)])
				elif (i-1,j) == enpassant_possible:
					valid_moves.append([(i,j),(i-1,j)])
							
				if j < 7:
					piece = board[i-1][j+1]
					if piece != '0':
						if not piece_pinned or pin_direction == (-1,1):
							if piece[0] != self.color:
								valid_moves.append([(i,j),(i-1,j+1)])
					elif (i-1,j+1) == enpassant_possible :
						valid_moves.append([(i,j),(i-1,j+1)])

				if 0 < j:
					piece = board[i-1][j-1]
					if piece != '0':
						if not piece_pinned or pin_direction == (-1,-1):
							if piece[0] != 'w':
								valid_moves.append([(i,j),(i-1,j-1)])
					elif (i-1,j-1) == enpassant_possible:
						valid_moves.append([(i,j),(i-1,j-1)])

			if i == 6 :
				piece = board[i-2][j]
				if board[i-1][j] == '0':
					if piece == '0':
						if not piece_pinned or pin_direction == (-1,0):	
							valid_moves.append([(i,j),(i-2,j)])

			return valid_moves

		else:
			if 7 > i :
				piece = board[i+1][j]
				if piece == '0':
					if not piece_pinned or pin_direction == (1,0):
						if piece[0] != self.color:
							valid_moves.append([(i,j),(i+1,j)])
				elif (i+1,j) == enpassant_possible:
					valid_moves.append([(i,j),(i+1,j)])					

				if j < 7:
					piece = board[i+1][j+1]
					if piece != '0':
						if not piece_pinned or pin_direction == (1,1):
							if piece[0] != self.color:
								valid_moves.append([(i,j),(i+1,j+1)])
					elif (i+1,j+1) == enpassant_possible:
						valid_moves.append([(i,j),(i+1,j+1)])		
				if 0 < j:
					piece = board[i+1][j-1]
					if piece != '0':
						if not piece_pinned or pin_direction == (1,-1):
							if piece[0] != self.color:
								valid_moves.append([(i,j),(i+1,j-1)])
					elif (i+1,j-1) == enpassant_possible:
						valid_moves.append([(i,j),(i+1,j-1)])		
				
			if i == 1 :
				piece = board[i+2][j]
				if board[i+1][j] == '0':
					if (not piece_pinned) or pin_direction == (1,0):
						if piece == '0':
							valid_moves.append([(i,j),(i+2,j)])
			
			return valid_moves


class Rook:
	def __init__(self,i,j,color):
		self.i = i
		self.j = j
		self.color = color[0]

	def valid_moves(self,board,pins):
		valid_moves = []
		i, j = self.i, self.j
		
		piece_pinned = False
		pin_direction = ()
		if pins:
			for k in range(len(pins)-1,-1,-1):
				if pins[k][0] == i and pins[k][1] == j:
					piece_pinned = True
					pin_direction = (pins[k][2],pins[k][3])
					break 

		#UP_MOVES
		for k in range(i-1,-1,-1):
			piece = board[k][j]
			if not piece_pinned or pin_direction[1] == 0 :
				if piece == '0':
					valid_moves.append([(i,j),(k,j)])
				elif piece[0] != self.color:
					valid_moves.append([(i,j),(k,j)])
					break
				else:
					break
		#DOWN_MOVES
		for k in range(i+1,8,1):
			piece = board[k][j]
			if not piece_pinned or pin_direction[1] == 0:
				if piece == '0':
					valid_moves.append([(i,j),(k,j)])
				elif piece[0] != self.color:
					valid_moves.append([(i,j),(k,j)])
					break
				else:
					break

		#RIGHT_MOVES
		for p in range(j+1,8,1):
			piece = board[i][p]
			if not piece_pinned or pin_direction[0] == 0 :	
				if piece == '0':
					valid_moves.append([(i,j),(i,p)])
				elif piece[0] != self.color:
					valid_moves.append([(i,j),(i,p)])
					break
				else:
					break

		#LEFT_MOVES
		for p in range(j-1,-1,-1):
			piece = board[i][p]
			if not piece_pinned or pin_direction[0] == 0:
				if piece == '0':
					valid_moves.append([(i,j),(i,p)])
				elif piece[0] != self.color:
					valid_moves.append([(i,j),(i,p)])
					break
				else:
					break

		return valid_moves

class Bishop:
	def __init__(self,i,j,color):
		self.i = i
		self.j = j
		self.color = color

	def valid_moves(self,board,pins):
		valid_moves = []
		i, j = self.i, self.j
		
		piece_pinned = False
		pin_direction = ()
		if pins:
			for k in range(len(pins)-1,-1,-1):
				if pins[k][0] == i and pins[k][1] == j:
					piece_pinned = True
					pin_direction = (pins[k][2],pins[k][3])
					break 

		#UP_RIGHT
		jUR = j
		for k in range(i-1,-1,-1):
			jUR += 1
			if jUR < 8:
				piece = board[k][jUR]
				if not piece_pinned or pin_direction == (-1,1) or pin_direction == (1,-1) :
					if piece == '0':
						valid_moves.append([(i,j),(k,jUR)])
					elif piece[0] != self.color:
						valid_moves.append([(i,j),(k,jUR)])
						break
					else:
						break
		#UP_LEFT
		jUL = j
		for k in range(i-1,-1,-1):
			jUL -= 1
			if jUL > -1:
				piece = board[k][jUL]
				if not piece_pinned or pin_direction == (-1,-1) or pin_direction == (1,1): 
					if piece == '0':
						valid_moves.append([(i,j),(k,jUL)])
					elif piece[0] != self.color:
						valid_moves.append([(i,j),(k,jUL)])
						break
					else:
						break
		#DOWN_RIGHT
		jDR = j
		for k in range(i+1,8,1):
			jDR += 1
			if jDR < 8:
				piece = board[k][jDR]
				if not piece_pinned or pin_direction == (1,1) or pin_direction == (-1,-1): 
					if piece == '0':
						valid_moves.append([(i,j),(k,jDR)])
					elif piece[0] != self.color:
						valid_moves.append([(i,j),(k,jDR)])
						break
					else:
						break
		#DOWN_LEFT
		jDL = j
		for k in range(i+1,8,1):
			jDL -= 1
			if jDL > -1:
				piece = board[k][jDL]
				if not piece_pinned or pin_direction == (1,-1) or pin_direction == (-1,1): 
					if piece == '0':
						valid_moves.append([(i,j),(k,jDL)])
					elif piece[0] != self.color:
						valid_moves.append([(i,j),(k,jDL)])
						break
					else:
						break

		return valid_moves

class Knight:
	def __init__(self,i,j,color):
		self.i = i
		self.j = j
		self.color = color

	def valid_moves(self,board,pins):
		i, j = self.i, self.j
		valid_moves = []
		
		piece_pinned = False
		pin_direction = ()
		if pins:
			for k in range(len(pins)-1,-1,-1):
				if pins[k][0] == i and pins[k][1] == j:
					piece_pinned = True
					pin_direction = (pins[k][2],pins[k][3])
					break

		if not piece_pinned:
			#TOP_RIGHT
			if i > 1 and j < 7:
				piece = board[i-2][j+1] 
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i-2,j+1)])
			if i > 0 and j < 6:	
				piece = board[i-1][j+2]
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i-1,j+2)])
			
			#TOP_LEFT
			if i > 1 and j > 0:
				piece = board[i-2][j-1] 
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i-2,j-1)])
			if i > 0 and j > 1:	
				piece = board[i-1][j-2]
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i-1,j-2)])
			
			#DOWN_RIGHT
			if i < 6 and j < 7:
				piece = board[i+2][j+1] 
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i+2,j+1)])
			if i < 7 and j < 6:	
				piece = board[i+1][j+2]
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i+1,j+2)])

			#DOWN_LEFT
			if i < 6 and j > 0:
				piece = board[i+2][j-1] 
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i+2,j-1)])
			if i < 7 and j > 1:	
				piece = board[i+1][j-2]
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i+1,j-2)])

		return valid_moves


class King:
	def __init__(self,i,j,color):
		self.i = i
		self.j = j
		self.color = color

	def valid_moves(self,board,checks):
		i, j = self.i, self.j
		valid_moves = []
		#RIGHT
		if j < 7:
			piece = board[i][j+1]
			if piece[0] != self.color:
				valid_moves.append([(i,j),(i,j+1)])
		#LEFT
		if j > 0:
			piece = board[i][j-1]
			if piece[0] != self.color:
				valid_moves.append([(i,j),(i,j-1)])
		#TOP
		if i > 0:
			piece = board[i-1][j]
			if piece[0] != self.color:
				valid_moves.append([(i,j),(i-1,j)])
		#DOWN
		if i < 7:
			piece = board[i+1][j]
			if piece[0] != self.color:
				valid_moves.append([(i,j),(i+1,j)])
		#TOP_RIGHT
		if i > 0 and j < 7:
			piece = board[i-1][j+1]
			if piece[0] != self.color:
				valid_moves.append([(i,j),(i-1,j+1)])
		#TOP_LEFT
		if i > 0 and j > 0:
			piece = board[i-1][j-1]
			if piece[0] != self.color:
				valid_moves.append([(i,j),(i-1,j-1)])
		#DOWN_LEFT
		if i < 7 and j > 0:
			piece = board[i+1][j-1]
			if piece[0] != self.color:
				valid_moves.append([(i,j),(i+1,j-1)])
		#DOWN_RIGHT
		if i < 7 and j < 7:
			piece = board[i+1][j+1]
			if piece[0] != self.color:
				valid_moves.append([(i,j),(i+1,j+1)])
			
		return valid_moves

	
class Queen:
	def __init__(self,i,j,color):
		self.i = i
		self.j = j
		self.color = color[0]

	def valid_moves(self,board,pins):
		i, j = self.i, self.j
		valid_moves = []
		piece_pinned = False
		pin_direction = ()
		if pins:
			for k in range(len(pins)-1,-1,-1):
				if pins[k][0] == i and pins[k][1] == j:
					piece_pinned = True
					pin_direction = (pins[k][2],pins[k][3])
					break


		#UP_RIGHT
		jUR = j
		for k in range(i-1,-1,-1):
			jUR += 1
			if jUR < 8:
				piece = board[k][jUR]
				if not piece_pinned or pin_direction == (-1,1) or pin_direction == (1,-1) :
					if piece == '0':
						valid_moves.append([(i,j),(k,jUR)])
					elif piece[0] != self.color:
						valid_moves.append([(i,j),(k,jUR)])
						break
					else:
						break
		#UP_LEFT
		jUL = j
		for k in range(i-1,-1,-1):
			jUL -= 1
			if jUL > -1:
				piece = board[k][jUL]
				if not piece_pinned or pin_direction == (-1,-1) or pin_direction == (1,1): 
					if piece == '0':
						valid_moves.append([(i,j),(k,jUL)])
					elif piece[0] != self.color:
						valid_moves.append([(i,j),(k,jUL)])
						break
					else:
						break
		#DOWN_RIGHT
		jDR = j
		for k in range(i+1,8,1):
			jDR += 1
			if jDR < 8:
				piece = board[k][jDR]
				if not piece_pinned or pin_direction == (1,1) or pin_direction == (-1,-1): 
					if piece == '0':
						valid_moves.append([(i,j),(k,jDR)])
					elif piece[0] != self.color:
						valid_moves.append([(i,j),(k,jDR)])
						break
					else:
						break
		#DOWN_LEFT
		jDL = j
		for k in range(i+1,8,1):
			jDL -= 1
			if jDL > -1:
				piece = board[k][jDL]
				if not piece_pinned or pin_direction == (-1,1) or pin_direction == (1,-1) :
					if piece == '0':
						valid_moves.append([(i,j),(k,jDL)])
					elif piece[0] != self.color:
						valid_moves.append([(i,j),(k,jDL)])
						break
					else:
						break

		#UP_MOVES
		for k in range(i-1,-1,-1):
			piece = board[k][j]
			if not piece_pinned or pin_direction[1] == 0 :
				if piece == '0':
					valid_moves.append([(i,j),(k,j)])
				elif piece[0] != self.color:
					valid_moves.append([(i,j),(k,j)])
					break
				else:
					break
		#DOWN_MOVES
		for k in range(i+1,8,1):
			piece = board[k][j]
			if not piece_pinned or pin_direction[1] == 0 :
				if piece == '0':
					valid_moves.append([(i,j),(k,j)])
				elif piece[0] != self.color:
					valid_moves.append([(i,j),(k,j)])
					break
				else:
					break

		#RIGHT_MOVES
		for p in range(j+1,8,1):
			piece = board[i][p]
			if not piece_pinned or pin_direction[0] == 0 :
				if piece == '0':
					valid_moves.append([(i,j),(i,p)])
				elif piece[0] != self.color:
					valid_moves.append([(i,j),(i,p)])
					break
				else:
					break
		
		#LEFT_MOVES
		for p in range(j-1,-1,-1):
			piece = board[i][p]
			if not piece_pinned or pin_direction[0] == 0 :
				if piece == '0':
					valid_moves.append([(i,j),(i,p)])
				elif piece[0] != self.color:
					valid_moves.append([(i,j),(i,p)])
					break
				else:
					break

		return valid_moves






