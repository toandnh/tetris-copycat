import arcade

from leaderboard import Leaderboard
from grid import Tetris
from sidebar import SideBar
from utilities import font_names


BACKGROUND_COLOR = (27, 27, 27)


class GameView(arcade.View):
    """ The game """
    def __init__(self):
        super().__init__()

        self.board_section = Leaderboard(0,
                                         0,
                                         self.window.width // 4,
                                         self.window.height,
                                         prevent_dispatch={False})
        self.game_section = Tetris(self.window.width // 4,
                                   0,
                                   1 * self.window.width // 2,
                                   self.window.height,
                                   accept_keyboard_events=True)
        self.sidebar_section = SideBar(3 * self.window.width // 4,
                                       0,
                                       self.window.width // 4,
                                       self.window.height,
                                       prevent_dispatch={False})

        self.section_manager.add_section(self.board_section)
        self.section_manager.add_section(self.game_section)
        self.section_manager.add_section(self.sidebar_section)

    def on_show_view(self):
        arcade.set_background_color(BACKGROUND_COLOR)

    def on_update(self, delta_time: float):
        self.sidebar_section.next_tetromino = self.game_section.next_tetromino
        self.sidebar_section.score = self.game_section.score
        self.sidebar_section.level = self.game_section.level
        self.sidebar_section.lines = self.game_section.lines

        if self.board_section.high_score < self.game_section.score:
            self.board_section.high_score = self.game_section.score
            self.board_section.new_high_score = True

        if self.board_section.new_high_score and self.game_section.game_over:
            self.board_section.update_high_score()

    def on_draw(self):
        self.clear()

        self.board_section.draw_board()
        self.game_section.draw_grid()
        self.sidebar_section.draw_sidebar()

        if self.game_section.game_over:
            arcade.draw_lrtb_rectangle_filled(left=0,
                                              right=self.window.width,
                                              top=self.window.height,
                                              bottom=0,
                                              color=arcade.color.GRAY + (220,))

            if self.board_section.new_high_score:
                arcade.draw_text('NEW HIGH SCORE',
                                 self.window.width // 2,
                                 6 * self.window.height // 10,
                                 arcade.color.BLACK,
                                 font_size=30,
                                 font_name=font_names,
                                 width=500,
                                 anchor_x='center')
                arcade.draw_text(f'- {self.board_section.high_score} -',
                                 self.window.width // 2,
                                 self.window.height // 2,
                                 arcade.color.BLACK,
                                 font_size=30,
                                 font_name=font_names,
                                 width=500,
                                 anchor_x='center')
            else:
                arcade.draw_text('GAME OVER',
                                 self.window.width // 2,
                                 6 * self.window.height // 10,
                                 arcade.color.BLACK,
                                 font_size=30,
                                 font_name=font_names,
                                 width=500,
                                 anchor_x='center')

            arcade.draw_text('press SPACE to start a new game',
                             self.window.width // 2,
                             12 * self.window.height // 30,
                             arcade.color.BLACK,
                             font_size=15,
                             font_name=font_names,
                             width=500,
                             anchor_x='center')
