import pygame as pg
import board
import sys

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = WIDTH // DIMENSION
MAX_FPS = 15
IMAGES = {}
dark, light = pg.Color("light blue"), pg.Color("white")
positions = []


class Chess :

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH,HEIGHT))
		pg.display.set_caption("Chess")
		self.clock = pg.time.Clock()
		
		self.gs = board.Board()

		#valid moves list
		self.valid_moves = self.gs.get_valid_moves()
		self.move_made = False # a move flag

		self._load_images() #load all images from the images file
		
		self.game_active = True #game state flag (active or not)
		
		self.square_selected = ()
		self.clicks, self.clicks_copy = [], []

		self.move_undoed = False

		#animation
		self.animate = False

		#Game Over
		self.game_over = False

	def run_game(self):
		while True :
			self._check_events()
			self._update_screen()
			
	def _check_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.game_active == False
				sys.exit()
			elif event.type == pg.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pg.MOUSEBUTTONDOWN:	
				if not self.game_over:
					mouse_pos = pg.mouse.get_pos()
					i, j = mouse_pos[1] // SQUARE_SIZE, mouse_pos[0] // SQUARE_SIZE
					if self.square_selected == (i,j): #if we select again on the same square
						self.square_selected = ()
						self.clicks = []
					else:
						self.square_selected = (i,j)
						self.clicks.append(self.square_selected)

					if len(self.clicks) == 2:
						self.gs.update_enpassant_possible(self.clicks[0],self.clicks[1])
						if [self.clicks[0],self.clicks[1]] in self.valid_moves:
							#if the move is valid
							self.gs.move_piece(self.clicks[0], self.clicks[1])
							self.move_made = True
							self.clicks_copy = self.clicks
							self.animate = True
							self.square_selected = ()
							self.clicks = []
							self.move_undoed = False

						else:
							#if we select another piece
							self.clicks = [self.square_selected]

		if self.move_made: #if the move is made generate the next list of valid moves
			if self.animate:
				if self.clicks_copy[1] not in self.gs.checked_squares :
					self.animate_move(self.clicks_copy[0],self.clicks_copy[1],self.screen,self.gs.board,self.clock)
			self.animate = False
			self.valid_moves = self.gs.get_valid_moves()
			self.move_made = False

		if self.gs.checkmate:
			self.game_over = True
			if self.gs.white_turn:
				self.draw_text(self.screen, 'Black wins by checkmate')
			else:
				self.draw_text(self.screen, 'White wins by checkmate')
		elif self.gs.stalemate:
			self.game_over = True
			self.draw_text(self.screen, 'Stalemate')


	def _check_keydown_events(self,event):
		if event.key == pg.K_a:
			sys.exit()
		elif event.key == pg.K_u:
			if self.move_undoed == False :
				self.gs.undo_move()
				self.move_made = True
				self.move_undoed = True
				self.animate = False
		elif event.key == pg.K_r:
			self.gs = board.Board()
			self.valid_moves = self.gs.get_valid_moves()
			self.move_made = False
			self.square_selected = ()
			self.clicks, self.clicks_copy = [], []
			self.move_undoed = False
			self.animate = False
			self.game_over = False


	def _load_images(self):
		pieces = ['bRook', 'bKnight', 'bBishop', 'bQueen', 'bKing', 'bPawn',
					'wRook', 'wKnight', 'wBishop', 'wQueen', 'wKing', 'wPawn']
		for piece in pieces:
			IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"),(SQUARE_SIZE,SQUARE_SIZE))

	def _draw_screen(self,board,valid_moves,square_selected):
		self._draw_board(self.screen)
		self.highlight_square(board,valid_moves,square_selected)
		self._draw_pieces(self.gs.board)


	def _draw_board(self,screen):
		global colors
		colors = [light, dark]
		for i in range(DIMENSION):
			for j in range(DIMENSION):
				pg.draw.rect(screen, colors[(i+j)%2], pg.Rect(j*SQUARE_SIZE,
					i*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

	def _draw_pieces(self,board):
		for i in range(DIMENSION):
			for j in range(DIMENSION):
				piece = board[i][j]
				if piece != "0":
					image = IMAGES[piece]
					rect = image.get_rect()
					rect.x, rect.y = j*SQUARE_SIZE, i*SQUARE_SIZE
					rect.width, rect.height = SQUARE_SIZE, SQUARE_SIZE
					self.screen.blit(image,rect)

	def highlight_square(self,board,valid_moves,square_selected):
		if square_selected != ():
			i, j = square_selected
			if board[i][j][0] == ('w' if self.gs.white_turn else 'b'):
				surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
				red_surface = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
				surface.set_alpha(100)
				red_surface.set_alpha(100)
				surface.fill(pg.Color('orange'))
				red_surface.fill(pg.Color('red'))
				self.screen.blit(surface,(j*SQUARE_SIZE, i*SQUARE_SIZE))
				surface.fill(pg.Color('green'))
				king_i, king_j = self.gs.white_king_location if self.gs.white_turn else self.gs.black_king_location
				#self.gs.get_checked_squares(king_i,king_j,self.valid_moves)
				for move in valid_moves:
					if move[0] == square_selected:
						end_i, end_j = move[1]
						if (move[1] not in self.gs.checked_squares and self.gs.board[move[0][0]][move[0][1]][1:] == 'King') or self.gs.board[move[0][0]][move[0][1]][1:] != 'King' :
							self.screen.blit(surface, (end_j*SQUARE_SIZE, end_i*SQUARE_SIZE))
						elif move[1] in self.gs.checked_squares :
							self.screen.blit(red_surface, (end_j*SQUARE_SIZE, end_i*SQUARE_SIZE))

	def animate_move(self,start,end,screen,board,clock):
		#self._load_images()
		global colors
		start_i, start_j = start[0], start[1]
		end_i, end_j = end[0], end[1]
		#piece_moved = board[start_i][start_j]
		#piece_captured = board[end_i][end_j]
		di = end_i - start_i
		dj = end_j - start_j
		frames_per_second = 10
		frame_count = ( abs(di) + abs(dj) ) * frames_per_second
		for frame in range(frame_count + 1):
			r, c = start_i+di*frame/frame_count, start_j+dj*frame/frame_count
			self._draw_board(screen)
			self._draw_pieces(board)
			color = colors[(end_i+end_j) % 2]
			end_square = pg.Rect(end_j*SQUARE_SIZE,end_i*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE)
			pg.draw.rect(screen, color, end_square)
			if self.gs.piece_captured != '0':
				if self.gs.enpassant_move:
					screen.blit(IMAGES[self.gs.piece_captured], pg.Rect(end_j*SQUARE_SIZE,start_i*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))	
				else:
					screen.blit(IMAGES[self.gs.piece_captured], end_square)
			screen.blit(IMAGES[self.gs.piece_moved], pg.Rect(c*SQUARE_SIZE,r*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
			pg.display.flip()
			clock.tick(60)

	def draw_text(self,screen,text):
		font = pg.font.SysFont('ms serif.ttf',40,True,True)
		text_object = font.render(text,0,pg.Color('White'))
		text_location = pg.Rect(0,0,WIDTH,HEIGHT).move(WIDTH/2-text_object.get_width()/2,HEIGHT/2-text_object.get_height()/2)
		self.screen.blit(text_object,text_location)
		text_object = font.render(text,0,pg.Color('Red'))
		self.screen.blit(text_object,text_location.move(2,2))
		pg.display.flip()
	
	def _update_screen(self):
		self._draw_screen(self.gs.board,self.valid_moves,self.square_selected)
		self.clock.tick(MAX_FPS)
		pg.display.flip()


if __name__ == '__main__':
	chess = Chess()
	chess.run_game()
