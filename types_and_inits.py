from constants import *

def grid_init(grid_size_x, grid_size_y):
    grid_line = [0 for i in range(grid_size_y)]
    grid = [grid_line.copy() for i in range(grid_size_x)]
    return grid

class position :
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    x = 0
    y = 0

class game :
    def __init__(self, names:list[str], player_count: int=DEFAULT_PLAYER_AMOUNT, grid_size: position=position(DEFAULT_GRID_SIZE[0], DEFAULT_GRID_SIZE[1]), winning_size:int=DEFALUT_WINNING_SIZE):
        self.player_count = player_count
        self.grid_size = grid_size
        self.winning_size = winning_size
        self.grid = grid_init(grid_size.x, grid_size.y)
        self.players = names
    
    players = []
    current_player = 1
    player_count = DEFAULT_PLAYER_AMOUNT
    grid_size = position(DEFAULT_GRID_SIZE[0],DEFAULT_GRID_SIZE[1])
    winning_size = DEFALUT_WINNING_SIZE
    grid = []

class vertical_positions :
    def __init__(self, question_position, warning_position, input_position):
        self.question_position = question_position
        self.warning_position = warning_position
        self.input_position = input_position
