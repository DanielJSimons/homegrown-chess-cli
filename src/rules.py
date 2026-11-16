class Rules:
    VALID_PIECES = frozenset({"q", "k", "b", "kn", "r", "p"})
    VALID_COLOURS = frozenset({"w", "b"})

    @classmethod
    def is_valid_piece(cls, piece: str) -> bool:
        return (piece[:1] in cls.VALID_COLOURS and piece[1:] in cls.VALID_PIECES)


    def possible_moves(self, board, from_square: tuple[int, int]) -> list[tuple[int, int]]:
        piece = board[from_square[0]][from_square[1]]

        if piece is None or not self.is_valid_piece(piece):
            return []

        move_methods = {
            "p": self.pawn_moves,
            "k": self.king_moves,
            "q": self.queen_moves,
            "b": self.bishop_moves,
            "r": self.rook_moves,
            "kn": self.knight_moves,
        }
        move_method = move_methods[piece[1:]]
        return move_method(board, from_square, piece)


    def check_occupied(self, board, to_square, piece) -> str | None:
        # we can check what is in that place and return the piece
        destination = board[to_square[0]][to_square[1]]

        if destination == None:
            return None

        if piece[:1] == destination[:1]:
            return "f"

        else:
            return "o"
    
    
    def pawn_moves(self, board, from_square, piece) -> list[tuple[int, int]]:
        if piece == "wp":
            direction = -1
            starting_row = 6
        else:
            direction = 1
            starting_row = 1

        row, column = from_square
        forward_row = row + direction

        if not 0 <= forward_row <= 7:
            return []

        moves = []
        forward_square = (forward_row, column)

        # Both squares must be empty to allow the initial two-square move.
        if self.check_occupied(board, forward_square, piece) is None:
            moves.append(forward_square)
            if row == starting_row:
                two_forward_square = (row + 2 * direction, column)
                if self.check_occupied(board, two_forward_square, piece) is None:
                    moves.append(two_forward_square)

        # Captures are independent of whether the forward square is blocked.
        for column_change in (-1, 1):
            capture_column = column + column_change
            if 0 <= capture_column <= 7:
                capture_square = (forward_row, capture_column)
                if self.check_occupied(board, capture_square, piece) == "o":
                    moves.append(capture_square)

        return moves


    def king_moves(self, board, from_square, piece) -> list[tuple[int, int]]:
        # The king can move to any in range unoccupied square within a radius of 1, including diagonally.
        # check that the square is not out of range first.
        if piece[1:] == "k": 
            rank, file = from_square
            moves = []

            for rank_change in (-1, 0, 1):
                for file_change in (-1, 0, 1):
                    possible_rank = rank + rank_change
                    possible_file = file + file_change

                    if 0 <= possible_rank <= 7 and 0 <= possible_file <= 7 and (possible_rank != rank or possible_file != file):
                        if self.check_occupied(board, (possible_rank, possible_file), piece) != "f":
                            moves.append((possible_rank, possible_file))
                        
            return moves
        return []


    def knight_moves(self, board, from_square, piece) -> list[tuple[int, int]]:
        if piece[1:] == "kn":
            directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2),  (1, 2), (2, -1),  (2, 1)]
            moves = []

            for rank_change, file_change in directions:
                possible_rank = from_square[0] + rank_change
                possible_file = from_square[1] + file_change

                if 0 <= possible_rank <= 7 and 0<= possible_file <= 7: 
                    if self.check_occupied(board, (possible_rank, possible_file), piece) != "f":
                        moves.append((possible_rank, possible_file))
            return moves
        return []


    def queen_moves(self, board, from_square, piece) -> list[tuple[int, int]]:
        """We can probably treat this similar to king but extend each direction to the barrier."""
        if piece[1:] == "q":
            directions = [(-1,-1), (1, 1), (-1, 1), (1, -1), (-1,0), (1, 0), (0, 1), (0, -1)]
            moves = self.move_projections(board, piece, from_square, directions)
            return moves
        return []

                    
    def rook_moves(self, board, from_square, piece) -> list[tuple[int, int]]:
        if piece[1:] == "r":
            directions = [(-1,0), (1, 0), (0, 1), (0, -1)]
            moves = self.move_projections(board, piece, from_square, directions)
            return moves
        return []


    def bishop_moves(self, board, from_square, piece) -> list[tuple[int, int]]:
        if piece[1:] == "b":
            directions = [(-1,-1), (1, 1), (-1, 1), (1, -1)]
            moves = self.move_projections(board, piece, from_square, directions)
            return moves
        return []


    def move_projections(self, board, piece, from_square, directions) -> list[tuple[int, int]]:
        rank, file = from_square
        moves = []
        for rank_change, file_change in directions:
            possible_rank = rank + rank_change
            possible_file = file + file_change

            while 0 <= possible_rank <= 7 and 0 <= possible_file <= 7:
                if self.check_occupied(board, (possible_rank, possible_file), piece) == None:
                    moves.append((possible_rank, possible_file))

                elif self.check_occupied(board,(possible_rank, possible_file), piece) == "f":
                    break

                elif self.check_occupied(board,(possible_rank, possible_file), piece) == "o":
                    moves.append((possible_rank, possible_file))
                    break

                possible_rank += rank_change
                possible_file += file_change
        return moves

    
    def king_check():
        pass

    
    def king_castle():
        pass

    
    def pawn_promotion():
        pass

    
    def pawn_en_passant():
        pass