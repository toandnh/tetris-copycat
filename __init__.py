import arcade

from menu_view import MenuView


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, 'Tetris Copycat', vsync=True, update_rate=1/120)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == '__main__':
    main()
