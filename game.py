import random

def nums_compressed(nums: list[int]) -> tuple[list[int], list[int]]:
    """Sums up consecutive pairs and returns new list and nums removed

    >>> nums_compressed([2, 2, 4, 4, 4, 8])
    ([4, 8, 4, 8], [2, 4])

    """
    # Processes nums as a stack with the first element at the top
    stack = nums[::-1]
    result = []
    removed = []
    # Until the stack is empty, check if the top 2 elements are the same
    while stack:
        if len(stack) < 2:
            result.append(stack.pop())
            continue
        if stack[-1] != stack[-2]:
            result.append(stack.pop())
            continue
        # Top 2 are the same. Add to removed list and sum them
        removed.append(stack[-1])
        result.append(stack.pop() + stack.pop())
    # Return the compressed list and the nums that were removed
    return result, removed

def grid_shifted(grid: list[list[int]]) -> tuple[list[list[int]], list[int]]:
    """Returns a new grid with 2048 left applied and nums removed

    >>> grid_shifted([[2, 0, 2], [4, 4, 4], [0, 2, 0]])
    ([[4, 0, 0], [8, 4, 0], [2, 0, 0]], [2, 4])

    """
    result = []
    removed = []
    for row in grid:
        zeroless = [num for num in row if num != 0]
        compressed, row_removed = nums_compressed(zeroless)
        compressed += [0] * (len(row) - len(compressed))  # Pad to row's length
        removed += row_removed
        result.append(compressed)
    return result, removed

def grid_transposed(grid: list[list[int]]) -> list[list[int]]:
    """Return grid with rows and columns swapped"""
    return [list(nums) for nums in zip(*grid)]

def grid_rows_reversed(grid: list[list[int]]) -> list[list[int]]:
    """Return grid with each row reversed"""
    return [row[::-1] for row in grid]

grid_shifted_left = grid_shifted

def grid_shifted_right(
    grid: list[list[int]],
) -> tuple[list[list[int]], list[int]]:
    shifted, removed = grid_shifted_left(grid_rows_reversed(grid))
    return grid_rows_reversed(shifted), removed

def grid_shifted_up(
    grid: list[list[int]],
) -> tuple[list[list[int]], list[int]]:
    shifted, removed = grid_shifted_left(grid_transposed(grid))
    return grid_transposed(shifted), removed

def grid_shifted_down(
    grid: list[list[int]],
) -> tuple[list[list[int]], list[int]]:
    shifted, removed = grid_shifted_right(grid_transposed(grid))
    return grid_transposed(shifted), removed

shift_functions = {
    "w": grid_shifted_up,
    "a": grid_shifted_left,
    "s": grid_shifted_down,
    "d": grid_shifted_right,
}

def is_game_over_grid(grid: list[list[int]]) -> bool:
    """Returns whether there is a move that results in something changing

    >>> is_game_over_grid([[2, 4], [4, 0]])
    False
    >>> is_game_over_grid([[2, 4], [4, 2]])
    True

    """
    return all(grid == func(grid)[0] for func in shift_functions.values())

def get_empty_positions(grid: list[list[int]]) -> list[tuple[int, int]]:
    """Returns (y, x) positions where the value is 0

    >>> get_empty_positions([[2, 4], [4, 0]])
    [(1, 1)]
    >>> get_empty_positions([[2, 4], [4, 2]])
    []

    """
    return [
        (y, x)
        for y, row in enumerate(grid)
        for x, num in enumerate(row)
        if num == 0
    ]

def grid_put(
    grid: list[list[int]],
    y: int,
    x: int,
    num: int,
) -> list[list[int]]:
    """Returns new grid with grid[y][x] == num and everything else the same

    >>> grid_put([[2, 4], [4, 0]], 1, 1, 2)
    [[2, 4], [4, 2]]

    """
    copy = [row.copy() for row in grid]
    copy[y][x] = num
    return copy

def grid_random_insert(grid: list[list[int]], num: int) -> list[list[int]]:
    """Returns new grid with a random empty element replaced by num

    >>> grid_random_insert([[2, 4], [4, 0]], 2)
    [[2, 4], [4, 2]]

    """
    empty = get_empty_positions(grid)
    assert len(empty) != 0
    y, x = random.choice(empty)
    return grid_put(grid, y, x, num)

def generate_random_insert_value() -> int:
    return 2 if random.random() < 0.9 else 4

# Game grid
width = 4
height = 4
grid = [[0] * width for _ in range(height)]

# Score increases by tile value from merging smaller tiles (2+2 == 4)
score = 0

# Game starts off with 2 tiles
grid = grid_random_insert(grid, generate_random_insert_value())
grid = grid_random_insert(grid, generate_random_insert_value())

# Game loop
while True:
    # Print grid and score
    for row in grid:
        print(*row, sep="\t")
    print(f"score: {score}")
    # End if game over
    if is_game_over_grid(grid):
        print("game over")
        break
    # Input loop
    while True:
        op = input("wasd> ")
        if op in shift_functions:
            # Go to next turn if the operation actually changes something
            if shift_functions[op](grid)[0] != grid:
                break
            continue
        print("unknown operation")
    # Shift grid and update score
    grid, removed = shift_functions[op](grid)
    score += sum(removed) * 2
    # Add random 2 or 4
    grid = grid_random_insert(grid, generate_random_insert_value())
