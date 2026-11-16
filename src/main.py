from board import Board
from rules import Rules


def main():
    board = Board()
    board.render_board()

    # White pawn advances two squares.
    board.select_piece((6, 3))
    input("Press Enter to move...")
    board.move_piece((6, 3), (4, 3))
    input("Press Enter to continue...")

    # Black pawn advances beside it.
    board.select_piece((1, 4))
    input("Press Enter to move...")
    board.move_piece((1, 4), (3, 4))
    input("Press Enter to continue...")

    # White pawn captures diagonally.
    board.select_piece((4, 3))
    input("Press Enter to move...")
    board.move_piece((4, 3), (3, 4))
    input("Press Enter to continue...")

    # Black develops a knight.
    board.select_piece((0, 6))
    input("Press Enter to move...")
    board.move_piece((0, 6), (2, 5))
    input("Press Enter to continue...")

    # White develops the bishop freed by its pawn.
    board.select_piece((7, 2))
    input("Press Enter to move...")
    board.move_piece((7, 2), (4, 5))
    input("Press Enter to continue...")

    board.render_board()
    print("Captured pieces:", board.taken_piece)

if __name__ == "__main__":
    main() 