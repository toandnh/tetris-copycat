import arcade
import random

from typing import List
from PIL import Image

from grid_functions import create_grid, collided, join_matrices, remove_row, rotate_clockwise
from utilities import tetromino_colors, tetromino_map


BOARD_HEIGHT = 20
BOARD_WIDTH = 10
CELL_SIZE = 30
MARGIN = 2
OFFSET = 250

points = [40, 100, 300, 1200]


def create_texture():
    """
    :return: list of textures
    """
    textures = []
    for color in tetromino_colors:
        img = Image.new('RGB', (CELL_SIZE, CELL_SIZE), color)
        textures.append(arcade.Texture(str(color), img))
    return textures


def create_grid_sprites(textures: List) -> arcade.SpriteList:
    """
    :return: a SpriteList of Sprites to go on screen
    """
    sprite_list = arcade.SpriteList(use_spatial_hash=False)

    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            sprite = arcade.Sprite()

            for texture in textures:
                sprite.append_texture(texture)

            sprite.set_texture(0)
            sprite.center_x = OFFSET + col * (CELL_SIZE + MARGIN)
            sprite.center_y = (BOARD_HEIGHT - row) * (CELL_SIZE + MARGIN)

            sprite_list.append(sprite)

    return sprite_list


def draw_tetromino(tetromino: List, offset_x: int, offset_y: int):
    """
    Draw the moving tetrominos
    :param tetromino:
    :param offset_x:
    :param offset_y:
    :return:
    """
    for row in range(len(tetromino)):
        for col in range(len(tetromino[0])):
            if tetromino[row][col]:
                color = tetromino_colors[tetromino[row][col]]

                x = OFFSET + (col + offset_x) * (CELL_SIZE + MARGIN)
                y = (BOARD_HEIGHT - row - offset_y) * (CELL_SIZE + MARGIN)

                arcade.draw_rectangle_filled(x, y, CELL_SIZE, CELL_SIZE, color)


class Tetris(arcade.Section):
    """ The place where the game takes place """
    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)

        self.next_tetromino = random.choice(tetromino_map)
        self.score = 0
        self.level = 0
        self.lines = 0

        self.tetromino = None
        self.tetromino_x = 0
        self.tetromino_y = 0

        self.textures = create_texture()
        self.grid_sprites = create_grid_sprites(self.textures)
        self.grid = create_grid(BOARD_WIDTH, BOARD_HEIGHT)

        self.update_grid_textures()

        self.new_tetromino()

        self.vertical_move_speed = 50
        self.horizontal_move_speed = 6
        self.drop_speed = 1

        self.frames = 0

        self.down_key_down = False
        self.left_key_down = False
        self.right_key_down = False

        self.game_over = False

    def new_tetromino(self):
        """
        Randomly choose a new tetromino and set its location to the top of the grid.
        If collided here, then game over.
        :return:
        """
        self.tetromino = self.next_tetromino
        self.next_tetromino = random.choice(tetromino_map)

        x = int(BOARD_WIDTH // 2 - len(self.tetromino[0]) // 2)
        y = 0

        if collided(self.grid, self.tetromino, (x, y)):
            self.game_over = True

        self.tetromino_x = x
        self.tetromino_y = y

    def drop(self):
        """
        Move the tetromino down one cell
        :return:
        """
        if not self.game_over:
            count = 0
            self.tetromino_y += 1
            if collided(self.grid, self.tetromino, (self.tetromino_x, self.tetromino_y)):
                self.grid = join_matrices(self.grid, self.tetromino, (self.tetromino_x, self.tetromino_y))
                while True:
                    for i, row in enumerate(self.grid):
                        if 0 not in row:
                            self.grid = remove_row(self.grid, i)
                            count += 1
                            break
                    else:
                        break

                if count:
                    self.score += points[count - 1] * (self.level + 1)
                    if self.lines % 10 + count >= 10:
                        self.vertical_move_speed -= 0 if self.vertical_move_speed == 8 else 2
                    self.lines += count
                    self.level = int(self.lines // 10)

                self.update_grid_textures()
                self.new_tetromino()

                self.down_key_down = False

    def update_grid_textures(self):
        """
        Update the sprite list to reflect the contents of the 2d grid
        :return:
        """
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                v = self.grid[row][col]
                loc = row * BOARD_WIDTH + col
                self.grid_sprites[loc].set_texture(v)

    def on_update(self, delta_time):
        self.frames += 1

        if self.frames % self.vertical_move_speed == 0:
            self.drop()

        if self.down_key_down:
            if self.frames % self.drop_speed == 0:
                self.drop()
        elif self.left_key_down and not self.right_key_down:
            if self.frames % self.horizontal_move_speed == 0:
                self.move_tetromino(-1)
        elif self.right_key_down and not self.left_key_down:
            if self.frames % self.horizontal_move_speed == 0:
                self.move_tetromino(1)

    def draw_grid(self):
        self.grid_sprites.draw()
        draw_tetromino(self.tetromino, self.tetromino_x, self.tetromino_y)

    def rotate_tetromino(self):
        """
        Rotate the tetromino clockwise
        :return:
        """
        if not self.game_over:
            rotated_tetromino = rotate_clockwise(self.tetromino)
            if self.tetromino_x + len(rotated_tetromino[0]) >= BOARD_WIDTH:
                self.tetromino_x = BOARD_WIDTH - len(rotated_tetromino[0])
            if not collided(self.grid, rotated_tetromino, (self.tetromino_x, self.tetromino_y)):
                self.tetromino = rotated_tetromino

    def move_tetromino(self, delta_x):
        """
        Move the tetrominoo
        :param delta_x:
        :return:
        """
        if not self.game_over:
            new_x = self.tetromino_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > BOARD_WIDTH - len(self.tetromino[0]):
                new_x = BOARD_WIDTH - len(self.tetromino[0])
            if not collided(self.grid, self.tetromino, (new_x, self.tetromino_y)):
                self.tetromino_x = new_x

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.rotate_tetromino()
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.down_key_down = True
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.left_key_down = True
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.right_key_down = True

        if self.game_over and symbol == arcade.key.SPACE:
            from menu_view import MenuView
            menu_view = MenuView()
            self.window.show_view(menu_view)

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.down_key_down = False
        elif symbol == arcade.key.LEFT or symbol == arcade.key.A:
            self.left_key_down = False
        elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
            self.right_key_down = False
