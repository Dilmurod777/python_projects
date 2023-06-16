import copy
import math
import random

levels = ["easy", "medium", "hard"]


class Board:
    def __init__(self, init_state):
        self.state = init_state
    
    def display(self):
        print('-' * 9)
        for row in self.state:
            line = "|"
            for el in row:
                line += f' {el.replace("_", " ").rjust(1, " ")}'
            line += ' |'
            print(line)
        
        print('-' * 9)
    
    def calculate_turn(self):
        num_x = sum([el == 'X' for row in self.state for el in row])
        num_o = sum([el == 'O' for row in self.state for el in row])
        
        return 0 if num_x <= num_o else 1
    
    def get_next_symbol(self):
        turn = self.calculate_turn()
        return 'X' if turn % 2 == 0 else 'O'
    
    def set_cell(self, coords, symbol):
        self.state[coords[0]][coords[1]] = symbol
    
    def check_coordinates(self, coords):
        # check if coordinates are valid
        for c in coords:
            if not c.isnumeric():
                print('You should enter numbers!')
                return False, []
        
        coords = [int(c) for c in coords]
        row = coords[0] - 1
        col = coords[1] - 1
        
        # check if valid coords
        if row > 2 or row < 0 or col > 2 or col < 0:
            print("Coordinates should be from 1 to 3!")
            return False, []
        
        # check if cell is occupied
        if self.state[row][col] != '_':
            print("This cell is occupied! Choose another one!")
            return False, []
        
        return True, [row, col]
    
    def get_state(self):
        # check all rows
        for row in self.state:
            joined_row = ''.join(row)
            if joined_row == 'XXX' or joined_row == 'OOO':
                return f"{joined_row[0]} wins"
                
                # check all cols
        for i in range(3):
            joined_col = ''.join([self.state[0][i], self.state[1][i], self.state[2][i]])
            if joined_col == 'XXX' or joined_col == 'OOO':
                return f"{joined_col[0]} wins"
        
        # check diagonal
        diagonal = ''.join([self.state[0][0], self.state[1][1], self.state[2][2]])
        if diagonal == 'XXX' or diagonal == 'OOO':
            return f"{diagonal[0]} wins"
        
        diagonal = ''.join([self.state[0][2], self.state[1][1], self.state[2][0]])
        if diagonal == 'XXX' or diagonal == 'OOO':
            return f"{diagonal[0]} wins"
        
        # check draw
        empty_cells = self.get_cells_with_symbol("_")
        if len(empty_cells) == 0:
            return 'Draw'
        
        # otherwise
        return None
    
    def get_cells_with_symbol(self, symbol):
        return [[i, j] for i in range(len(self.state)) for j in range(len(self.state[i])) if self.state[i][j] == symbol]


class User:
    def __init__(self, mark):
        self.mark = mark
    
    def move(self, board):
        while True:
            user_coords = input("Enter the coordinates: ").strip().replace('  ', ' ').split(' ')
            valid, coords = board.check_coordinates(user_coords)
            if valid:
                return coords


class AI:
    def __init__(self, level, mark, silent=False):
        self.level = level
        self.silent = silent
        self.mark = mark
    
    def move(self, board):
        if not self.silent:
            print(f'Making move level "{self.level}"')
        if self.level == "easy":
            empty_cells = board.get_cells_with_symbol('_')
            return random.choice(empty_cells)
        elif self.level == "medium":
            # check rows for win in 1 move
            for i in range(3):
                combination = ''.join(board.state[i])
                empty_cell_idx = combination.find('_')
                if (combination.count('X') == 2 or combination.count('O') == 2) and empty_cell_idx != -1:
                    return [i, empty_cell_idx]
            
            # check cols for win in 1 move
            for i in range(3):
                combination = ''.join([board.state[0][i], board.state[1][i], board.state[2][i]])
                empty_cell_idx = combination.find('_')
                if (combination.count('X') == 2 or combination.count('O') == 2) and empty_cell_idx != -1:
                    return [empty_cell_idx, i]
            
            # check diagonals for win in 1 move
            diagonal = ''.join([board.state[0][0], board.state[1][1], board.state[2][2]])
            empty_cell_idx = diagonal.find('_')
            if (diagonal.count('X') == 2 or diagonal.count('O') == 2) and empty_cell_idx != -1:
                return [empty_cell_idx, empty_cell_idx]
            
            diagonal = ''.join([board.state[0][2], board.state[1][1], board.state[2][0]])
            empty_cell_idx = diagonal.find('_')
            if (diagonal.count('X') == 2 or diagonal.count('O') == 2) and empty_cell_idx != -1:
                return [empty_cell_idx, 2 - empty_cell_idx]
            
            # random play
            empty_cells = board.get_cells_with_symbol('_')
            return random.choice(empty_cells)
        elif self.level == "hard":
            empty_cells = board.get_cells_with_symbol('_')
            # return random.choice(empty_cells)
            best_score = -math.inf
            best_move = None
            for ec in empty_cells:
                board.set_cell(ec, board.get_next_symbol())
                score = minimax(board, self.mark, False)
                board.set_cell(ec, '_')
                if score > best_score:
                    best_score = score
                    best_move = ec
            
            return best_move


def minimax(board, mark, is_maximizing):
    state = board.get_state()
    
    if state is not None and state == "Draw":
        return 0
    
    if state is not None:
        return 100 if state[0] == mark else -100
    
    scores = []
    for move in board.get_cells_with_symbol('_'):
        board.set_cell(move, board.get_next_symbol())
        scores.append(minimax(board, mark, not is_maximizing))
        board.set_cell(move, '_')
    
    return max(scores) if is_maximizing else min(scores)


class Game:
    number_of_games = 0
    
    def __init__(self, board, players, silent=False):
        self.board = board
        self.players = players
        self.turn = self.board.calculate_turn()
        self.silent = silent
    
    def play(self):
        if not self.silent:
            self.board.display()
        while True:
            state = self.board.get_state()
            if state is not None:
                if not self.silent:
                    print(state)
                return
            
            coords = self.players[0].move(self.board)
            self.board.set_cell(coords, self.players[0].mark)
            self.turn = self.board.calculate_turn()
            if not self.silent:
                self.board.display()
            state = self.board.get_state()
            if state is not None:
                if not self.silent:
                    print(state)
                return
            
            coords = self.players[1].move(self.board)
            self.board.set_cell(coords, self.players[1].mark)
            self.turn = self.board.calculate_turn()
            if not self.silent:
                self.board.display()
            state = self.board.get_state()
            if state is not None:
                if not self.silent:
                    print(state)
                return


while True:
    command = input("Input command: ")
    command = command.split(' ')
    if command[0] == 'start':
        params = command[1:]
        if len(params) != 2:
            print("Bad parameters!")
            continue
        if not all([p == 'user' or p in levels for p in params]):
            print("Bad parameters!")
            continue
        
        board = Board([['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']])
        player1 = User('X') if params[0] == 'user' else AI(params[0], 'X')
        player2 = User('O') if params[1] == 'user' else AI(params[1], 'O')
        Game(board, [player1, player2], False).play()
    elif command[0] == 'exit':
        break
    else:
        print('Invalid command!')
