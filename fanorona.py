from random import randint
import numpy as np


class Board:
    def __init__(self, board_width, board_height):
        self.width = board_width
        self.height = board_height
        self.board = self.generate_board(board_width, board_height)

    def generate_board(self, board_width, board_height):
        board = [[0] * board_width for _ in range(board_height)]
        # 3x3
        if board_width == 3 and board_height == 3:
            board[1][0] = 1
            board[1][1] = -1
            for i in range(board_width):
                board[2][i] = 1
        # 5x5
        elif board_width == 5 and board_height == 5:
            board[2][1] = 1
            board[2][2] = -1
            board[2][4] = 1
            for i in range(board_width):
                board[3][i] = 1
            for i in range(board_width):
                board[4][i] = 1
        # 9x5
        elif board_width == 9 and board_height == 5:
            board[2][1] = 1
            board[2][3] = 1
            board[2][4] = -1
            board[2][6] = 1
            board[2][8] = 1
            for i in range(board_width):
                board[3][i] = 1
            for i in range(board_width):
                board[4][i] = 1
        return board

    def is_empty_space(self, x_cor, y_cor):
        return self.board[y_cor][x_cor] == -1

    def get_player(self, x_cor, y_cor):
        return self.board[y_cor][x_cor]

    def assign_space(self, x_cor, y_cor, player):
        self.board[y_cor][x_cor] = player

    def get_surrounding_spaces(self, x_curr, y_curr):
        surrounding_coords = [
            (x_curr - 1, y_curr - 1),
            (x_curr, y_curr - 1),
            (x_curr - 1, y_curr),
            (x_curr + 1, y_curr),
            (x_curr, y_curr + 1),
            (x_curr + 1, y_curr + 1),
            (x_curr - 1, y_curr + 1),
            (x_curr + 1, y_curr - 1),
        ]
        coords_in_bounds = [
            (x, y)
            for x, y in surrounding_coords
            if 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1
        ]
        return coords_in_bounds

    def is_valid_coord(self, x_coord, y_coord):
        return 0 <= x_coord <= self.width - 1 and 0 <= y_coord <= self.height - 1

    def get_all_piece_coords(self, player):
        coords = []
        for y in range(self.height):
            for x in range(self.width):
                if self.get_player(x, y) == player:
                    coord = (x, y)
                    coords.append(coord)
        return coords

    def is_retreat(self, x_curr, y_curr, x_new, y_new, player):
        opponent = 1 if player == 0 else 0
        # retreat
        x_coord_in_line = x_new - 2 * (x_new - x_curr)
        y_coord_in_line = y_new - 2 * (y_new - y_curr)
        return (
            self.is_valid_coord(x_coord_in_line, y_coord_in_line)
            and self.get_player(x_coord_in_line, y_coord_in_line) == opponent
        )

    def get_all_valid_moves(self, player):
        moves = {}
        all_pieces = self.get_all_piece_coords(player)
        for coord in all_pieces:
            valid_moves = self.get_valid_moves(*coord, player)
            moves[coord] = valid_moves
        return {item: moves.get(item) for item in moves if moves.get(item) != []}

    def get_valid_moves(self, x_curr, y_curr, player):
        opponent = 1 if player == 0 else 0
        valid_moves = []
        surrounding_coords = self.get_surrounding_spaces(x_curr, y_curr)
        open_space_coords = [
            (x, y)
            for x, y in surrounding_coords
            if self.get_player(x, y) != player and self.is_empty_space(x, y)
        ]
        # check if opponent is in line of space you're taking
        for coord in open_space_coords:
            # attacking
            x_coord_in_line = coord[0] + (coord[0] - x_curr)
            y_coord_in_line = coord[1] + (coord[1] - y_curr)
            if (
                self.is_valid_coord(x_coord_in_line, y_coord_in_line)
                and self.get_player(x_coord_in_line, y_coord_in_line) == opponent
            ):
                valid_moves.append(coord)
            # retreat
            x_coord_in_line = coord[0] - 2 * (coord[0] - x_curr)
            y_coord_in_line = coord[1] - 2 * (coord[1] - y_curr)
            if (
                self.is_valid_coord(x_coord_in_line, y_coord_in_line)
                and self.get_player(x_coord_in_line, y_coord_in_line) == opponent
            ):
                valid_moves.append(coord)
        return valid_moves

    def can_move_piece(self, x_curr, y_curr, x_new, y_new, player):
        return (x_new, y_new) in self.get_valid_moves(x_curr, y_curr, player)

    def make_move_and_claim_pieces(self, x_curr, y_curr, x_new, y_new, player):
        opponent = 1 if player == 0 else 0
        if self.can_move_piece(x_curr, y_curr, x_new, y_new, player):
            self.assign_space(x_new, y_new, player)
            self.assign_space(x_curr, y_curr, -1)
            if self.is_retreat(x_curr, y_curr, x_new, y_new, player):
                if self.is_retreat(x_curr, y_curr, x_new, y_new, player):
                    x_coord_in_line = x_new - 2 * (x_new - x_curr)
                    y_coord_in_line = y_new - 2 * (y_new - y_curr)
                else:
                    x_coord_in_line = x_new + (x_new - x_curr)
                    y_coord_in_line = y_new + (y_new - y_curr)
                while (
                    self.is_valid_coord(x_coord_in_line, y_coord_in_line)
                    and not self.is_empty_space(x_coord_in_line, y_coord_in_line)
                    and self.get_player(x_coord_in_line, y_coord_in_line) == opponent
                ):
                    self.assign_space(x_coord_in_line, y_coord_in_line, -1)
                    x_coord_in_line = x_coord_in_line - (x_new - x_curr)
                    y_coord_in_line = y_coord_in_line - (y_new - y_curr)
        else:
            print("cant move")
        print(np.matrix(self.board))

    def play_game_random_moves(self):
        while (
            len(self.get_all_valid_moves(0)) != 0
            and len(self.get_all_valid_moves(1)) != 0
        ):
            if len(self.get_all_valid_moves(1)) > 0:
                move = randint(0, len(list(self.get_all_valid_moves(1).keys())) - 1)
                piece_can_move = list(self.get_all_valid_moves(1).keys())[move]
                move_chosen = randint(
                    0, len(self.get_all_valid_moves(1).get(piece_can_move)) - 1
                )
                print(
                    f"Player 1 moving piece {piece_can_move} to {self.get_all_valid_moves(1).get(piece_can_move)[move_chosen]}"
                )
                self.make_move_and_claim_pieces(
                    *piece_can_move,
                    *self.get_all_valid_moves(1).get(piece_can_move)[move_chosen],
                    1,
                )
            if len(self.get_all_valid_moves(0)) > 0:
                move = randint(0, len(list(self.get_all_valid_moves(0).keys())) - 1)
                piece_can_move = list(self.get_all_valid_moves(0).keys())[move]
                move_chosen = randint(
                    0, len(self.get_all_valid_moves(0).get(piece_can_move)) - 1
                )
                print(
                    "Player 0 moving piece ",
                    piece_can_move,
                    "to ",
                    self.get_all_valid_moves(0).get(piece_can_move)[move_chosen],
                )
                self.make_move_and_claim_pieces(
                    *piece_can_move,
                    *self.get_all_valid_moves(0).get(piece_can_move)[0],
                    0,
                )

        if len(self.get_all_piece_coords(1)) == 0:
            print("0 wins the game")
        elif len(self.get_all_piece_coords(0)) == 0:
            print("1 wins the game")
        else:
            print("game is a draw")


class Fanorona:
    def __init__(self, board_height, board_width):
        self.board = Board(board_height=board_height, board_width=board_width)


if __name__ == "__main__":
    board = Board(9, 5)
    print(np.matrix(board.board))
    board.play_game_random_moves()
