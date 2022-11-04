import arcade

from utilities import font_names


class MenuView(arcade.View):
    """ Class that manages the menu view """
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

    def on_draw(self):
        self.clear()
        arcade.draw_text('Welcome to Tetris Copycat',
                         self.window.width // 2,
                         6 * self.window.height // 10,
                         arcade.color.BLACK,
                         font_size=30,
                         font_name=font_names,
                         width=500,
                         anchor_x='center')
        arcade.draw_text('press SPACE to start',
                         self.window.width // 2,
                         14 * self.window.height // 30,
                         arcade.color.BLACK,
                         font_size=15,
                         font_name=font_names,
                         width=500,
                         anchor_x='center')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            from game_view import GameView
            game_view = GameView()
            self.window.show_view(game_view)
