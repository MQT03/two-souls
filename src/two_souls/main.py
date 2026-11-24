
from two_souls.presentation.game import Game
from two_souls.simulation.session import create_new_game


def main() -> None:
    session = create_new_game()

    game = Game(session)
    game.run()


if __name__ == "__main__":
    main()
