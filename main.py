
from board import Board

def main():
    board = Board(base=3)
    board.run()
    print("Board:")
    board.pretty_prints(board.board)
    print("Solved board:")
    board.pretty_prints(board.SolvedBoard)


if __name__ == "__main__":
    main()