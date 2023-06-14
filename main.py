from logic import CarcassonneGame
from view.game import GameView


def main():
    game = CarcassonneGame.from_file_and_names(
        "assets/default_tileset", ["Alice", "Bob"]
    )
    view = GameView()
    view.run()


if __name__ == "__main__":
    main()
