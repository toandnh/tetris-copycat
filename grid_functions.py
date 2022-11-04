from typing import List


def create_grid(row: int, col: int) -> List:
    """
    Create a two-dimensional grid.
    :param row:
    :param col:
    :return:
    """
    return [[0 for _ in range(row)] for _ in range(col)]


def rotate_clockwise(tetromino: List):
    """
    Rotate a tetromino clockwise
    :param tetromino:
    :return:
    """
    return [[tetromino[y][x] for y in range(len(tetromino))]
            for x in range(len(tetromino[0]) - 1, -1, -1)]


def collided(grid: List, tetromino: List, offset: tuple):
    """
    Check for collision between tetrominos or tetromino and the bottom wall
    :param grid:
    :param tetromino:
    :param offset:
    :return:
    """
    offset_x, offset_y = offset
    for y, row in enumerate(tetromino):
        for x, cell in enumerate(row):
            if y + offset_y > len(grid) - 1 or cell and grid[y + offset_y][x + offset_x]:
                return True
    return False


def remove_row(grid: List, row: int):
    """
    Remove the row at the given index
    :param grid:
    :param row: index of the to be removed row
    :return: the given grid with:
                - given row removed, and
                - a row of 0s add on top
    """
    del grid[row]
    return [[0 for _ in range(len(grid[0]))]] + grid


def join_matrices(matrix1: List, matrix2: List, matrix2_offset: tuple) -> List:
    """
    Copy matrix2 into matrix1 based on the given offset
    :param matrix1:
    :param matrix2:
    :param matrix2_offset:
    :return:
    """
    offset_x, offset_y = matrix2_offset
    for y, row in enumerate(matrix2):
        for x, cell in enumerate(row):
            matrix1[y + offset_y - 1][x + offset_x] += cell
    return matrix1


