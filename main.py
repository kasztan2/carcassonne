from logic import CarcassonneGame


def main():
    game = CarcassonneGame.from_file_and_names(
        "assets/default_tileset", ["Alice", "Bob"]
    )


if __name__ == "__main__":
    main()
