import copy

O = [[4, 14, 15, 5]]
I = [[4, 14, 24, 34], [3, 4, 5, 6]]
S = [[5, 4, 14, 13], [4, 14, 15, 25]]
Z = [[4, 5, 15, 16], [5, 15, 14, 24]]
L = [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]]
J = [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]]
T = [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]

DEFAULT_STATES = {
    'O': O,
    'I': I,
    'S': S,
    'Z': Z,
    'L': L,
    'J': J,
    'T': T,
}


class Grid:
    COLS = 10
    ROWS = 10
    EMPTY_CELL = '-'
    OCCUPIED_CELL = '0'
    
    def __init__(self):
        self.board = []
        self.pieces = []
        self.curr_piece = None
        self.game_over = False
    
    def init(self):
        for i in range(Grid.ROWS):
            self.board.append([])
            for j in range(Grid.COLS):
                self.board[-1].append(Grid.EMPTY_CELL)
    
    def empty_grid(self):
        for i in range(Grid.ROWS):
            for j in range(Grid.COLS):
                self.board[i][j] = Grid.EMPTY_CELL
    
    def display(self):
        for i in range(Grid.ROWS):
            for j in range(Grid.COLS):
                print(self.board[i][j], end='')
                if j != Grid.COLS - 1:
                    print(' ', end='')
            print('\n', end='')
        print('\n', end='')
    
    def update_board(self):
        for piece in self.pieces:
            for el in piece.states[piece.curr_state_idx]:
                if el == -1:
                    continue
                i = (piece.curr_y + el // Piece.COLS) % Grid.ROWS
                j = (piece.curr_x + el % Piece.COLS) % Grid.COLS
                self.board[i][j] = Grid.OCCUPIED_CELL
    
    def add(self, piece):
        self.update_board()
        self.pieces.append(piece)
        self.curr_piece = piece
        self.update_board()
    
    def break_board(self):
        for i in range(Grid.ROWS):
            row = self.board[i]
            if ''.join(row) == Grid.OCCUPIED_CELL * Grid.COLS:
                for j in range(i, 0, -1):
                    self.board[j] = copy.copy(self.board[j - 1])
                self.board[0] = [Grid.EMPTY_CELL for x in range(Grid.COLS)]
        
        for i in range(Grid.ROWS):
            for j in range(Grid.COLS):
                if self.board[i][j] == Grid.OCCUPIED_CELL:
                    continue
                
                for piece in self.pieces:
                    for eli in range(len(piece.states[piece.curr_state_idx])):
                        el = piece.states[piece.curr_state_idx][eli]
                        pi = (piece.curr_y + el // Piece.COLS) % Grid.ROWS
                        pj = (piece.curr_x + el % Piece.COLS) % Grid.COLS
                        
                        if pi == i and pj == j:
                            piece.hide_cell(eli)
    
    def is_available(self, p, pi, pj):
        for piece in self.pieces:
            if piece.id != p.id:
                for el in piece.states[piece.curr_state_idx]:
                    i = (piece.curr_y + el // Piece.COLS) % Grid.ROWS
                    j = (piece.curr_x + el % Piece.COLS) % Grid.COLS
                    if i == pi and j == pj:
                        return False
        
        return True


class Piece:
    ROWS = 4
    COLS = 10
    NUMS = 0
    
    def __init__(self, value):
        self.value = value
        self.curr_x = 0
        self.curr_y = 0
        self.states = copy.deepcopy(DEFAULT_STATES[value])
        self.curr_state_idx = 0
        self.fixed = False
        self.id = Piece.NUMS
        Piece.NUMS += 1
    
    def hide_cell(self, eli):
        self.states[self.curr_state_idx][eli] = -1
    
    def can_move_left(self):
        if self.fixed:
            return False
        
        for el in self.states[self.curr_state_idx]:
            i = (self.curr_y + el // Piece.COLS) % Grid.ROWS
            j = (self.curr_x + el % Piece.COLS) % Grid.COLS
            
            if i == Grid.ROWS - 1:
                self.fixed = True
                return False
            
            if j == 0:
                return False
        
        return True
    
    def can_move_right(self):
        if self.fixed:
            return False
        
        for el in self.states[self.curr_state_idx]:
            i = (self.curr_y + el // Piece.COLS) % Grid.ROWS
            j = (self.curr_x + el % Piece.COLS) % Grid.COLS
            
            if i == Grid.ROWS - 1:
                self.fixed = True
                return False
            
            if j == Grid.COLS - 1:
                return False
        
        return True
    
    def can_move_down(self):
        if self.fixed:
            return False
        
        for el in self.states[self.curr_state_idx]:
            i = (self.curr_y + el // Piece.COLS) % Grid.ROWS
            j = (self.curr_x + el % Piece.COLS) % Grid.COLS
            
            if i == Grid.ROWS - 1 or not grid.is_available(self, i + 1, j):
                self.fixed = True
                return False
        
        return True
    
    def check_end_game(self):
        all_fixed = True
        for piece in grid.pieces:
            if not piece.fixed:
                all_fixed = False
                break
        
        if all_fixed:
            if any([x == Grid.OCCUPIED_CELL for x in grid.board[0]]):
                grid.game_over = True
                return
    
    def left(self):
        self.free_prev_cells()
        if self.can_move_left():
            self.curr_x = (self.curr_x - 1) % Grid.COLS
        if self.can_move_down():
            self.curr_y = (self.curr_y + 1) % Grid.ROWS
        
        grid.update_board()
        self.check_end_game()
    
    def right(self):
        self.free_prev_cells()
        if self.can_move_right():
            self.curr_x = (self.curr_x + 1) % Grid.COLS
        if self.can_move_down():
            self.curr_y = (self.curr_y + 1) % Grid.ROWS
        
        grid.update_board()
        self.check_end_game()
    
    def down(self):
        self.free_prev_cells()
        if self.can_move_down():
            self.curr_y = (self.curr_y + 1) % Grid.ROWS
        
        grid.update_board()
        self.check_end_game()
    
    def rotate(self):
        self.free_prev_cells()
        if self.can_move_down():
            self.curr_state_idx = (self.curr_state_idx + 1) % len(self.states)
        if self.can_move_down():
            self.curr_y = (self.curr_y + 1) % Grid.ROWS
        grid.update_board()
        
        self.check_end_game()
    
    def free_prev_cells(self):
        for el in self.states[self.curr_state_idx]:
            i = (self.curr_y + el // Piece.COLS) % Grid.ROWS
            j = (self.curr_x + el % Piece.COLS) % Grid.COLS
            grid.board[i][j] = Grid.EMPTY_CELL


grid = Grid()

dimensions = [int(x) for x in input().split(' ')]
Grid.COLS = dimensions[0]
Grid.ROWS = dimensions[1]
grid.init()

while True:
    grid.display()
    if grid.game_over:
        print("Game Over!")
        break
    
    command = input()
    
    if command == 'exit':
        break
    elif command == 'left':
        if grid.curr_piece is not None:
            grid.curr_piece.left()
    elif command == 'right':
        if grid.curr_piece is not None:
            grid.curr_piece.right()
    elif command == 'down':
        if grid.curr_piece is not None:
            grid.curr_piece.down()
    elif command == 'rotate':
        if grid.curr_piece is not None:
            grid.curr_piece.rotate()
    elif command == 'piece':
        p = Piece(input())
        grid.add(p)
    elif command == 'break':
        grid.break_board()
