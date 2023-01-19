import types_and_inits
import functions
import time
"""
game = types_and_inits.game()
start = time.time()
print(functions.count_points(game))
end = time.time()
print(end - start)
"""

"""
grid = types_and_inits.grid_init()
print(grid)

game = types_and_inits.game()

functions.show_grid(game)
"""

"""grid_1 = [  [1,1,1,1,2],
            [2,1,1,1,2],
            [2,1,1,1,1],
            [2,2,2,2,2],
            [2,2,2,2,2]]
"""
grid_1 = [  [1,1,1,1,2],
            [2,1,1,1,2],
            [2,1,1,1,1],
            [2,1,2,1,2],
            [2,1,2,2,2]]

grid_1 = [  [1,1,1,2,1],
            [2,1,1,1,2],
            [2,2,1,1,1],
            [2,1,2,1,1],
            [2,1,2,2,1]]

grid_1 = [  [1,1,1,1,1],
            [2,1,1,1,2],
            [2,1,1,2,1],
            [1,1,2,1,1],
            [1,2,2,2,1]]
            
game = types_and_inits.game(["a","b"])
game.grid = grid_1

functions.show_grid(game)

print(functions.count_points(game))

"""
while True:
    functions.round(game)
"""

