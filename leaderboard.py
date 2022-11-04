import arcade

from utilities import font_names


FONT_SIZE = 18


class Leaderboard(arcade.Section):
    def __init__(self, left: int, bottom: int, width: int, height: int, **kwargs):
        super().__init__(left, bottom, width, height, **kwargs)

        with open('high-score.txt', 'r') as f:
            lines = f.readlines()

        self.high_score = int(lines[0])
        self.new_high_score = False

    def update_high_score(self):
        with open('high-score.txt', 'w') as f:
            f.write(str(self.high_score))

    def draw_board(self):
        arcade.draw_lrtb_rectangle_filled(self.left,
                                          self.right - 10,
                                          self.top - 50,
                                          self.bottom + 500,
                                          arcade.color.WHITE_SMOKE)
        arcade.draw_text('High Score',
                         self.left + 25,
                         self.height - 100,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)
        arcade.draw_text(f'{self.high_score}',
                         self.left + 50,
                         self.height - 150,
                         arcade.color.BLACK,
                         FONT_SIZE,
                         font_name=font_names)
