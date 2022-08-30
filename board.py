from piece import *


ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
rows_to_ranks = {v:k for k,v in ranks_to_rows.items()}

letters_to_columns = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
columns_to_letters = {v:k for k,v in letters_to_columns.items()}



class CastleRights:
	"""class for Castling Rights"""
	def __init__(self,wks,wqs,bks,bqs):
		self.wks = wks
		self.wqs = wqs
		self.bks = bks
		self.bqs = bqs	



class Board:
	def __init__(self):
		self.board = [
		['bRook', 'bKnight', 'bBishop', 'bQueen', 'bKing', 'bBishop', 'bKnight', 'bRook'],
		['bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn', 'bPawn'],
		['0', '0', '0', '0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0', '0', '0', '0'],
		['0', '0', '0', '0', '0', '0', '0', '0'],
		['wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn', 'wPawn'],
		['wRook', 'wKnight', 'wBishop', 'wQueen', 'wKing', 'wBishop', 'wKnight', 'wRook']
					]
		
		self.white_turn = True
		self.move_log = []
		self.piece_captured, self.piece_moved= '', ''
		self.class_functions = {'Pawn':Pawn,'Rook':Rook,'Knight':Knight,'Bishop':Bishop,'Queen':Queen,'King':King}
		
		#Checkmate variables
		self.black_king_location, self.white_king_location = (0,4), (7,4)
		self.in_check, self.pins, self.checks = False, [], []
		self.checked_squares = []
		self.checkmate = False
		self.stalemate = False

		#Pawn promotion
		self.promoted = False

		#En passant
		self.enpassant_move, self.white_enpassant_possible, self.black_enpassant_possible = False, (), ()
		self.enpassant_move_made = False

		#Castling
		self.current_castling_rights = CastleRights(True,True,True,True)
		self.castle_rights_log = [CastleRights(self.current_castling_rights.wks,
									self.current_castling_rights.wqs,
									self.current_castling_rights.bks,
									self.current_castling_rights.bqs)]
		self.is_castle_move = False


	def move_piece(self,start_pos,end_pos):
		#self.piece_captured, self.piece_moved= '', ''
		start_i, start_j = start_pos[0], start_pos[1]
		end_i, end_j = end_pos[0], end_pos[1]
		
		piece_moved, move_made = self.board[start_i][start_j], False

		#Pawn promotion
		pawn_promotion = False
		self.promoted = False
		
		#Enpassant
		self.enpassant_move_made, self.enpassant_move = False, False

		#castling
		self.is_castle_move, self.castle_move_made = False, False

		#Update king location
		self.update_king_location(start_pos,end_pos)

		in_check, pins, checks = self.pins_and_checks()

		if self.board[start_i][start_j][1:] =='King':
			self.get_castle_moves(start_i,start_j,self.get_valid_moves())
			#Castle move
			if self.is_castle_move:
				self.castle_move(start_pos,end_pos)
				move_made = True 

			if not in_check:
				self.piece_captured = self.board[end_i][end_j]
				self.piece_moved = self.board[start_i][start_j]
				self.board[end_i][end_j] = self.board[start_i][start_j]
				self.board[start_i][start_j] = '0'
				self.move_log.append(self._get_chess_notation(start_i,start_j,end_i,end_j))
				print(self._get_chess_notation(start_i,start_j,end_i,end_j))
				print(self.white_king_location, self.black_king_location)
				move_made = True 

			else:
				if self.board[start_i][start_j][0] == 'w':
					self.white_king_location = (start_i,start_j)

				elif self.board[start_i][start_j][0] == 'b':
					self.black_king_location = (start_i,start_j)


		else:
			if (self.board[start_i][start_j] == 'wPawn' and end_i == 0) or \
				(self.board[start_i][start_j] == 'bPawn' and end_i == 7):
				pawn_promotion = True

			if self.white_enpassant_possible != () and self.black_enpassant_possible != ():
				if (self.board[start_i][start_j] == 'wPawn' and (end_i,end_j) == (2,self.white_enpassant_possible[1]) ) or \
						(self.board[start_i][start_j] == 'bPawn' and (end_i,end_j) == (5,self.black_enpassant_possible[1]) ) :
					self.enpassant_move = True


			#Enpassant move
			if self.enpassant_move:
				self.piece_captured = self.board[start_i][end_j]
				self.piece_moved = self.board[start_i][start_j]
				self.board[start_i][end_j] = '0'
				self.board[end_i][end_j] = self.board[start_i][start_j]
				self.board[start_i][start_j] = '0'
				self.move_log.append(self._get_chess_notation(start_i,start_j,end_i,end_j))
				print(self._get_chess_notation(start_i,start_j,end_i,end_j))
				self.previous_enpassant_possible = self.white_enpassant_possible if self.board[start_i][start_j][0] == 'w' else self.black_enpassant_possible
				if self.board[start_i][start_j][0] == 'w':
					self.white_enpassant_possible = ()
				elif self.board[start_i][start_j][0] == 'b':
					self.black_enpassant_possible = ()
				self.enpassant_move_made = True
				move_made = True 

			else:
				self.piece_captured = self.board[end_i][end_j]
				self.piece_moved = self.board[start_i][start_j]
				piece_color = self.board[start_i][start_j][0]
				self.board[end_i][end_j] = self.board[start_i][start_j]
				self.board[start_i][start_j] = '0'
				self.move_log.append(self._get_chess_notation(start_i,start_j,end_i,end_j))
				print(self._get_chess_notation(start_i,start_j,end_i,end_j))
				move_made = True 

				if pawn_promotion:
					#self.piece_captured = self.board[end_i][end_j]
					#self.piece_moved = self.board[start_i][start_j]
					self.board[end_i][end_j] = piece_color + 'Queen'
					self.promoted = True
					move_made = True 

		'''Update Castling Rights after making the move'''
		self.update_castling_rights(start_pos,piece_moved)
		self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks,
									self.current_castling_rights.wqs,
									self.current_castling_rights.bks,
									self.current_castling_rights.bqs))


		if move_made:
			self.white_turn = not self.white_turn
			self.checked_squares = []


	def undo_move(self):
		if len(self.move_log) != 0:
			start_pos_i = ranks_to_rows[self.move_log[-1][1]]
			start_pos_j = letters_to_columns[self.move_log[-1][0]]

			end_pos_i = ranks_to_rows[self.move_log[-1][7]]
			end_pos_j = letters_to_columns[self.move_log[-1][6]]

			'''Undo Castling Rights'''
			self.castle_rights_log.pop() #remove castle rights from the move we undo
			#set the current castle rights to the last one from the new modified log
			self.current_castling_rights.wks = self.castle_rights_log[-1].wks
			self.current_castling_rights.wqs = self.castle_rights_log[-1].wqs
			self.current_castling_rights.bks = self.castle_rights_log[-1].bks
			self.current_castling_rights.bqs = self.castle_rights_log[-1].bqs
			

			'''Reset king location to the previous one'''
			self.update_king_location((end_pos_i,end_pos_j),(start_pos_i,start_pos_j))

			if self.promoted == True:
				self.board[start_pos_i][start_pos_j] = self.board[end_pos_i][end_pos_j][0] + 'Pawn'
				self.board[end_pos_i][end_pos_j] = self.piece_captured
				del self.move_log[-1]
				self.promoted = False

			elif self.enpassant_move_made:
				self.board[start_pos_i][start_pos_j] = self.board[end_pos_i][end_pos_j]
				self.board[end_pos_i][end_pos_j] = '0'
				self.board[start_pos_i][end_pos_j] = self.piece_captured
				del self.move_log[-1]
				self.enpassant_move = False		
				#self.enpassant_possible = self.previous_enpassant_possible
				self.enpassant_move_made = False

			elif self.castle_move_made:
				if ( end_pos_j - start_pos_j )== 2: #kingside castle moves
					if self.board[end_pos_i][end_pos_j-1][1:] == 'Rook':
						self.board[end_pos_i][end_pos_j+1] = self.board[end_pos_i][end_pos_j-1]
						self.board[end_pos_i][end_pos_j-1] = '0'

				else: #queenside castle move
					if self.board[end_pos_i][end_pos_j+1][1:] == 'Rook':
						self.board[end_pos_i][end_pos_j-2] = self.board[end_pos_i][end_pos_j+1]
						self.board[end_pos_i][end_pos_j+1] = '0'

				self.board[start_pos_i][start_pos_j] = self.board[end_pos_i][end_pos_j]
				self.board[end_pos_i][end_pos_j] = '0'
			
			else:
				self.board[start_pos_i][start_pos_j] = self.board[end_pos_i][end_pos_j]
				self.board[end_pos_i][end_pos_j] = self.piece_captured
				del self.move_log[-1]

			self.white_turn = not self.white_turn

			print(self.white_king_location, self.black_king_location)
			

	def _get_chess_notation(self,start_i,start_j,end_i,end_j):
		return str(columns_to_letters[start_j]+rows_to_ranks[start_i]+" to "+columns_to_letters[end_j]+rows_to_ranks[end_i])

	def get_valid_moves(self):
		all_valid_moves = []
		L = []

		if self.white_turn:
			king_i = self.white_king_location[0]
			king_j = self.white_king_location[1]
			color = 'w'

		else:
			king_i = self.black_king_location[0]
			king_j = self.black_king_location[1]
			color = 'b'

		self.in_check, self.pins, self.checks = self.pins_and_checks()

		if self.in_check:
			if len(self.checks) == 1: # 1 possible check
				all_valid_moves = self.get_possible_moves(self.pins,self.checks,self.white_enpassant_possible if self.white_turn else self.black_enpassant_possible)
				check = self.checks[0]
				check_i = check[0]
				check_j = check[1]
				piece_checking = self.board[check_i][check_j]
				valid_squares = [] #squares that piece can move to

				#if piece checking is knight we should capture it or move the king, otherwise we just block the piece
				if piece_checking[1:] == 'Knight':
					valid_squares = [(check_i, check_j)]
				else:
					for i in range(1,8):
						valid_square = (king_i + check[2] * i, king_j + check[3] * i)
						valid_squares.append(valid_square)
						if valid_square[0] == check_i and valid_square[1] == check_j:
							#once we get to the piece checking we stop
							break

				#get rid of any movements that doesen't block check or move king
				for i in range(len(all_valid_moves)-1,-1,-1):
					if all_valid_moves[i][0] != (king_i,king_j): #that means the move doesen't move the king,so it must block or capture
						if not (all_valid_moves[i][1][0],all_valid_moves[i][1][1]) in valid_squares:
							all_valid_moves.remove(all_valid_moves[i])
			
			else: #Double checks
				king = King(king_i,king_j,color)
				all_valid_moves = king.valid_moves(self.board,self.checks)
		
		else: #not in check, all moves are good
			all_valid_moves = self.get_possible_moves(self.pins,self.checks,self.white_enpassant_possible if self.white_turn else self.black_enpassant_possible)

		print(self.pins, self.in_check, self.checks)

		self.get_castle_moves(king_i,king_j,all_valid_moves)

		self.get_checked_squares(king_i,king_j,all_valid_moves)

		if abs(len(all_valid_moves) - len(self.checked_squares)) == 0 or len(all_valid_moves) == 0 :
			if self.in_check:
				self.checkmate = True
			else:
				self.stalemate = True
		else:
			self.checkmate = False
			self.stalemate = False

		#self.get_checkmate(king_i, king_j, all_valid_moves)

		return all_valid_moves

		
	def get_possible_moves(self,pins,checks,enpassant_possible):
		moves = []
		for i in range(8):
			for j in range(8):
				color = self.board[i][j][0]
				if (color == 'w' and self.white_turn) or (color == 'b' and not self.white_turn):
					piece = self.board[i][j][1:]
					piece_instance = self.class_functions[piece](i,j,color)
					if piece == 'King':
						if piece_instance.valid_moves(self.board,checks):
							for move in piece_instance.valid_moves(self.board,checks):
								moves.append(move)

					elif piece == 'Pawn':
						if piece_instance.valid_moves(self.board,pins,enpassant_possible):
							for move in piece_instance.valid_moves(self.board,pins,enpassant_possible):
								moves.append(move)

					else:
						if piece_instance.valid_moves(self.board,pins):
							for move in piece_instance.valid_moves(self.board,pins):
								moves.append(move)
		return moves

	def pins_and_checks(self):
		pins, checks, in_check = [], [], False
		if self.white_turn:
			enemy_color = 'b'
			ally_color = 'w'
			king_i = self.white_king_location[0]
			king_j = self.white_king_location[1]
		else:
			enemy_color = 'w'
			ally_color = 'b'
			king_i = self.black_king_location[0]
			king_j = self.black_king_location[1]
		
		directions = ((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
		
		for j in range(len(directions)):
			d = directions[j]
			possible_pin = ()
			for i in range(1,8):
				row = king_i + d[0] * i
				col = king_j + d[1] * i
				if 0 <= row < 8 and 0 <= col < 8:
					piece = self.board[row][col]
					if piece[0] == ally_color and piece[1:] != 'King' :
						if possible_pin == ():
							possible_pin = (row, col, d[0], d[1])
						else:
							break
					elif piece[0] == enemy_color:
						type = piece[1:]
						
						#There are 5 possibilities of checking directions on king depending on the type of the piece
						#1. orthogonally and piece is rook
						#2. diagonally and piece is bishop
						#3. 1 square diagonally and piece is pawn
						#4. Every direction and piece is queen
						#5. king squares

						if ( 0 <= j <=3 and type == 'Rook') or \
								( 4 <= j <= 7 and type == 'Bishop') or \
								( i == 1 and type == 'Pawn' and ((enemy_color == 'w' and 6 <= j <= 7 ) or (enemy_color == 'w' and 4 <= j <= 5 ))) or \
								(type == 'Queen') or (i == 1 and type == 'King'):
							if possible_pin == (): #No piece is blocking then it's a check
								checks.append((row,col,d[0],d[1]))
								in_check = True
								break
							else: #A piece is actually blocking so it's a pin 
								pins.append(possible_pin)
								break
						else: #No piece is checking
							break
				
				else:  #Off board
					break

		#There's actually a sixth possibility which is knight is checking
		kinght_movs = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
		for m in kinght_movs:
			row = king_i + m[0]
			col = king_j + m[1]
			if 0 <= row <= 7 and 0 <= col <= 7:
				piece = self.board[row][col]
				if piece[0] == enemy_color and piece[1:] == 'Knight':
					in_check = True
					checks.append((row,col,m[0],m[1]))

		return in_check,pins,checks


	def update_enpassant_possible(self,start,end):
		'''Update enpassant_possible variable'''
		start_i, start_j = start[0], start[1]
		end_i, end_j = end[0], end[1]
		if (self.board[start_i][start_j] == 'wPawn' and self.white_turn and abs(start_i - end_i) == 2) :
			self.black_enpassant_possible = ((start_i + end_i)//2, start_j)
		elif (self.board[start_i][start_j] == 'bPawn' and not self.white_turn and abs(start_i - end_i) == 2):
			self.white_enpassant_possible = ((start_i + end_i)//2, start_j)
		
	def update_castling_rights(self,start,piece_moved):
		''' Update castling rights depending on the move made '''
		start_i, start_j = start[0], start[1]
		if piece_moved == 'wKing':
			self.current_castling_rights.wqs = False
			self.current_castling_rights.wks = False
		
		elif piece_moved == 'bKing':
			self.current_castling_rights.bqs = False
			self.current_castling_rights.bks = False

		elif piece_moved == 'wRook':
			if start_i == 7:
				if start_j == 0: #left rook
					self.current_castling_rights.wqs = False
				if start_j == 7: #right rook
					self.current_castling_rights.wks = False
					
		elif piece_moved == 'bRook':
			if start_i == 0:
				if start_j == 0: #left rook
					self.current_castling_rights.bqs = False
				if start_j == 7: #right rook
					self.current_castling_rights.bks = False
					
	def get_castle_moves(self,i,j,valid):
		if self.square_under_attack(i,j):
			pass #can't caste while in check
		
		if (self.white_turn and self.current_castling_rights.wks) or (not self.white_turn and self.current_castling_rights.bks):
			self.get_kingside_castle_moves(i,j,valid)
		
		if (self.white_turn and self.current_castling_rights.wqs) or (not self.white_turn and self.current_castling_rights.bqs):
			self.get_queenside_castle_moves(i,j,valid)


	def get_kingside_castle_moves(self,i,j,valid):
		if j == 4:
			if self.board[i][j+1] == '0' and self.board[i][j+2] == '0':
				if ( self.square_under_attack(i,j+1) != True ) and ( self.square_under_attack(i,j+2) != True ):
					valid.append([(i,j),(i,j+2)])
					self.is_castle_move = True

	def get_queenside_castle_moves(self,i,j,valid):
		if j == 4:	
			if self.board[i][j-1] == '0' and self.board[i][j-2] == '0':
				if ( self.square_under_attack(i,j-1) != True ) and ( self.square_under_attack(i,j-2) != True):
					valid.append([(i,j),(i,j-2)]) 
					self.is_castle_move = True

	def square_under_attack(self,i,j):
		self.white_turn = not self.white_turn
		opp_moves = self.get_possible_moves(self.pins,self.checks,self.white_enpassant_possible if self.white_turn else self.black_enpassant_possible)
		self.white_turn = not self.white_turn
		for l in opp_moves:	
			if self.white_turn:
				if (i,j) == l[1] and self.board[l[0][0]][l[0][1]][0] == 'b':  
					return True
					break
			else:
				if (i,j) == l[1] and self.board[l[0][0]][l[0][1]][0] == 'w':  
					return True
					break
	
	def update_king_location(self, start, end):
		start_i, start_j = start[0], start[1]
		end_i, end_j = end[0], end[1]
		if self.board[start_i][start_j] == 'wKing':
			self.white_king_location = (end_i,end_j)

		elif self.board[start_i][start_j] == 'bKing':
			self.black_king_location = (end_i,end_j)

	def castle_move(self,start,end):
		start_i, start_j = start[0], start[1]
		end_i, end_j = end[0], end[1]
		self.piece_moved = self.board[start_i][start_j]
		if ( end_j - start_j ) == 2: #kingside castle moves
			if self.board[end_i][end_j+1][1:] == 'Rook': 
				self.board[end_i][end_j-1] = self.board[end_i][end_j+1]
				self.board[end_i][end_j+1] = '0'

		else: #queenside castle move
			if self.board[end_i][end_j-2][1:] == 'Rook': 
				self.board[end_i][end_j+1] = self.board[end_i][end_j-2]
				self.board[end_i][end_j-2] = '0'

		self.is_castle_move = False
		self.castle_move_made = True

	def get_checked_squares(self,king_i,king_j,valid_moves):
		#self.white_turn = not self.white_turn
		#opp_moves = self.get_possible_moves(self.pins,self.checks,self.white_enpassant_possible if self.white_turn else self.black_enpassant_possible)
		#self.white_turn = not self.white_turn
		'''directions = [(1,0),(-1,0),(-1,1),(0,1),(0,-1),(1,1),(-1,-1),(1,-1)]
		for d in directions:
			i,j = king_i + d[0], king_j + d[1]
			if self.square_under_attack(i,j):
				valid_moves.remove([(king_i,king_j),(i,j)])'''
		for k in range(len(valid_moves)-1,-1,-1):
			move = valid_moves[k]
			if move[0] == (king_i,king_j):
				if self.board[king_i][king_j] == 'wKing':
					self.white_king_location = move[1]
				elif self.board[king_i][king_j] == 'bKing':
					self.black_king_location = move[1]
				#self.update_king_location((king_i,king_j),move[1])
				
				in_check ,pins, checks = self.pins_and_checks()
				if in_check:
					self.checked_squares.append(move[1])
				
				if self.board[king_i][king_j] == 'wKing':
					self.white_king_location = (king_i,king_j)
				elif self.board[king_i][king_j] == 'bKing':
					self.black_king_location = (king_i,king_j)

	def get_checkmate(self,king_i,king_j,valid):
		king_valid_moves = []
		k = 0
		in_check, pins, checks = self.pins_and_checks()
		for move in valid:
			if move[0] == (king_i,king_j):
				king_valid_moves.append(move[1])
		
		for m in king_valid_moves:
			i,j = m
			if self.square_under_attack(i,j):
				k += 1
		if in_check:
			if k == len(king_valid_moves):
				self.checkmate = True		



'''class King:
	def __init__(self,i,j,color,):
		self.i = i
		self.j = j
		self.color = color
		self.gs = Board()

	def valid_moves(self,board,checks):
		i, j = self.i, self.j
		valid_moves = []
		#RIGHT
		if j < 7:
			piece = board[i][j+1]
			if self.color =='w':
				self.white_king_location = (i,j+1)
			else:
				self.black_king_location = (i,j+1)
			in_check,pins,checks = self.gs.pins_and_checks()
			if not in_check:
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i,j+1)])
			else:
				if self.color =='w':
					self.white_king_location = (i,j)
				else:
					self.black_king_location = (i,j)
		#LEFT
		if j > 0:
			piece = board[i][j-1]
			if self.color =='w':
				self.white_king_location = (i,j-1)
			else:
				self.black_king_location = (i,j-1)
			in_check,pins,checks = self.gs.pins_and_checks()
			if not in_check:
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i,j-1)])
			else:
				if self.color =='w':
					self.white_king_location = (i,j)
				else:
					self.black_king_location = (i,j)
		if i > 0:
			piece = board[i-1][j]
			if self.color =='w':
				self.white_king_location = (i-1,j)
			else:
				self.black_king_location = (i-1,j)
			in_check,pins,checks = self.gs.pins_and_checks()
			if not in_check:
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i-1,j)])
			else:
				if self.color =='w':
					self.white_king_location = (i,j)
				else:
					self.black_king_location = (i,j)
		#DOWN
		if i < 7:
			piece = board[i+1][j]
			if self.color =='w':
				self.white_king_location = (i+1,j)
			else:
				self.black_king_location = (i+1,j)
			in_check,pins,checks = self.gs.pins_and_checks()
			if not in_check:
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i+1,j)])
			else:
				if self.color =='w':
					self.white_king_location = (i,j)
				else:
					self.black_king_location = (i,j)
		#TOP_RIGHT
		if i > 0 and j < 7:
			piece = board[i-1][j+1]
			if self.color =='w':
				self.white_king_location = (i-1,j+1)
			else:
				self.black_king_location = (i-1,j+1)
			in_check,pins,checks = self.gs.pins_and_checks()
			if not in_check:
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i-1,j+1)])
			else:
				if self.color =='w':
					self.white_king_location = (i,j)
				else:
					self.black_king_location = (i,j)
		#TOP_LEFT
		if i > 0 and j > 0:
			piece = board[i-1][j-1]
			if self.color =='w':
				self.white_king_location = (i-1,j-1)
			else:
				self.black_king_location = (i-1,j-1)
			in_check,pins,checks = self.gs.pins_and_checks()
			if not in_check:
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i-1,j-1)])
			else:
				if self.color =='w':
					self.white_king_location = (i,j)
				else:
					self.black_king_location = (i,j)
		#DOWN_LEFT
		if i < 7 and j > 0:
			piece = board[i+1][j-1]
			if self.color =='w':
				self.white_king_location = (i+1,j-1)
			else:
				self.black_king_location = (i+1,j-1)
			in_check,pins,checks = self.gs.pins_and_checks()
			if not in_check:
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i+1,j-1)])
			else:
				if self.color =='w':
					self.white_king_location = (i,j)
				else:
					self.black_king_location = (i,j)
		#DOWN_RIGHT
		if i < 7 and j < 7:
			piece = board[i+1][j+1]
			if self.color =='w':
				self.white_king_location = (i+1,j+1)
			else:
				self.black_king_location = (i+1,j+1)
			in_check,pins,checks = self.gs.pins_and_checks()
			if not in_check:
				if piece[0] != self.color:
					valid_moves.append([(i,j),(i+1,j+1)])
			else:
				if self.color =='w':
					self.white_king_location = (i,j)
				else:
					self.black_king_location = (i,j)
			
		return valid_moves
'''


