import random

def generate_random_numbers():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    random.shuffle(numbers)
    return numbers

def solve(grid):
    empty = find_empty(grid)
    if empty==None:return grid
    row, col = empty
    numbers=generate_random_numbers()
    for num in range(0, 9):
        number=numbers[num]
        if valid(grid, number, (row, col)):
            grid[row][col] = number
            if solve(grid):return grid
            grid[row][col] = 0
    return None

def generate_grid():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    holes = random.randint(65, 75)
    solve(grid)
    solution = [row.copy() for row in grid]  # create a copy of grid to preserve solution
    while holes > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0
        holes -= 1
    return grid,solution

def valid(grid, num, pos):
    row, col = pos
    for i in range(9):
        if grid[row][i] == num and i != col:
            return False
        if grid[i][col] == num and i != row:
            return False
        box_row = (row // 3) * 3 + i // 3
        box_col = (col // 3) * 3 + i % 3
        if grid[box_row][box_col] == num and (box_row != row or box_col != col):
            return False
    return True

def find_empty(grid):
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return i, j
    return None

def print_grid(grid):
    if not grid: return
    print('-'*20)
    for lines in grid:
        l = ''
        for col in lines:
            l = l + str(col)+" "
        print(l)

def check_unique_solution(grid,solution):
    # Check if the grid is already solved
    
    if all(all(cell != 0 for cell in row) for row in grid):
        return True
    
    # Try filling each empty cell with each possible valid number
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                for k in range(1, 10):
                    if valid(grid,k,(i,j)):
                        grid[i][j] = k
                        test_grid = [row.copy() for row in grid]  # create a copy of grid to preserve initial grid
                        solved_grid=solve(test_grid)
                        if solved_grid is not None and solved_grid != solution:
                            # There is more than one solution
                            return False
                        # None of the possible numbers worked, so backtrack
                        grid[i][j] = 0
    return True

def generate_sudoku():
    unique_solution = False
    essai = 1
    while not unique_solution:
        grid=[]
        solution=[]
        grid,solution = generate_grid()
        initial_grid = [row.copy() for row in grid]  # create a copy of grid to preserve initial grid
        initial_solution=[row.copy() for row in solution ] #create a copy of the solution to preserve the original solution
        print('*' * 20,"essai=" + str(essai))
        print_grid(initial_grid)
        print
        print_grid(initial_solution)
        if check_unique_solution(grid,solution):
            return initial_grid,initial_solution
        essai += 1

def main():
    grid,solution = generate_sudoku()
if __name__ == '__main__':
    main()