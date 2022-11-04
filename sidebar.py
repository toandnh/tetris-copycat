import arcade

from utilities import tetromino_colors, font_names


FONT_SIZE = 18


class SideBar(arcade.Section):
    """ The panel on the right to display relevant information """
    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)

        self.next_tetromino = None
        self.score = 0
        self.level = 0
        self.lines = 0

    def draw_sidebar(self):
        arcade.draw_lrtb_rectangle_filled(self.left,
                                          self.right,
                                          self.top,
                                          self.bottom,
                                          arcade.color.WHITE_SMOKE)
        arcade.draw_text('Next',
                         self.left + 25,
                         self.height - 50,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)
        if self.next_tetromino is not None:
            for row in range(len(self.next_tetromino)):
                for col in range(len(self.next_tetromino[0])):
                    color = tetromino_colors[self.next_tetromino[row][col]]
                    if not self.next_tetromino[row][col]:
                        color = arcade.color.WHITE_SMOKE
                    arcade.draw_lrtb_rectangle_filled(self.left + 70 + 22 * col,
                                                      self.left + 70 + 22 * col + 20,
                                                      self.height - 90 - 22 * row,
                                                      self.height - 90 - 22 * row - 20,
                                                      color=color)

        arcade.draw_text('Score',
                         self.left + 25,
                         3 * (self.height - 50) // 4,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)
        arcade.draw_text(f'{self.score}',
                         self.left + 50,
                         3 * (self.height - 50) // 4 - 50,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)

        arcade.draw_text('Level',
                         self.left + 25,
                         (self.height - 50) // 2,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)
        arcade.draw_text(f'{self.level}',
                         self.left + 50,
                         (self.height - 50) // 2 - 50,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)

        arcade.draw_text('Lines',
                         self.left + 25,
                         (self.height - 50) // 4,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)
        arcade.draw_text(f'{self.lines}',
                         self.left + 50,
                         (self.height - 50) // 4 - 50,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)
