# Author: Brent Thomas
# Date: 11/20/21
# Description: This is a program that runs a Hasami Shogi Game, based on variant 1, where there are only one type of
#              piece and a two person game.

class HasamiShogiGame:
    """
    This class creates a new Hasami Shogi Game to be played by two players.
    """

    def __init__(self):
        """
        This initializes the game, creates the game board with all pieces in their starting locations, initializes the
        game_state to be 'UNFINISHED', active_player to be 'BLACK', which is the first player to go,
        black_captured = 0 and red_captured = 0
        """

        self._game_board = [["R", "R", "R", "R", "R", "R", "R", "R", "R"], [".", ".", ".", ".", ".", ".", ".", ".", "."],
                            [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."],
                            [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."],
                            [".", ".", ".", ".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", ".", ".", ".", "."],
                            ["B", "B", "B", "B", "B", "B", "B", "B", "B"]]
        self._game_state = "UNFINISHED"
        self._active_player = "BLACK"
        self._black_captured = 0
        self._red_captured = 0

    def get_game_state(self):
        """
        This checks the current state of the game, returns 'UNFINISHED', 'RED_WON', or 'BLACK_WON'
        :return:
        """

        return self._game_state

    def get_active_player(self):
        """
        This method checks which player's turn it is and return either 'RED' or 'BLACK'
        :return:
        """

        return self._active_player

    def get_num_captured_pieces(self, player):
        """
        Takes one parameter, 'RED' or 'BLACK' and returns the number of pieces of that color that have been captured.
        :param player:
        :return:
        """

        if player == "RED":
            return self._red_captured

        if player == "BLACK":
            return self._black_captured

    def update_game_state(self):
        """
        This is a helper function that checks the current game state after a move has been made and updates the game
        state if necessary
        :return:
        """

        if self._black_captured >= 8:
            self._game_state = "RED_WON"

        if self._red_captured >= 8:
            self._game_state = "BLACK_WON"

    def convert_board_notation(self, board_location):
        """
        This is a helper function that takes the algebraic input from the user and converts it into a usable tuple that
        can be used to index into the game board.[The tuple is (row, column)] Various methods use this including,
        make_move, get_square_occupant
        :param board_location:
        :return:
        """
        board_location_row = board_location[0]
        board_location_column = board_location[1]
        rows = "abcdefghi"
        row_counter = 0
        row_tuple = None

        for letter in rows:
            if letter == board_location_row:
                row_tuple = row_counter
            row_counter += 1

        square_tuple = (row_tuple, int(board_location_column)-1)

        return square_tuple

    def get_square_occupant(self, square_location):
        """
        This takes one parameter 'square_location', and returns 'RED','BLACK' or 'NONE', depending on what is in the
        passed square_location.
        :param square_location:
        :return:
        """

        square = self.convert_board_notation(square_location)   # sends the input parameter to the helper function and returns the usable tuple (row, column)
        square_occupant = self._game_board[square[0]][square[1]]

        if square_occupant == "R":
            return "RED"
        elif square_occupant == "B":
            return "BLACK"
        else:
            return "NONE"

    def make_move(self, moved_from, moved_to):
        """
        This function takes two parameters, strings that represent the square moved from and the square moved to.
        For example, make_move('b3', 'b9'). If the square being moved from does not contain a piece belonging to the
        player whose turn it is, or if the indicated move is not legal, or if the game has already been won, then it
        should just return False. Otherwise it should make the indicated move, remove any captured pieces, update the
        game state if necessary, update whose turn it is, and return True.
        :param moved_from: String in algebraic notation of a piece location to move
        :param moved_to: String in algebraic notation of a piece to move to this location
        :return:
        """

        if self._game_state != "UNFINISHED":
            #print("False, game state")
            return False

        if self._active_player != self.get_square_occupant(moved_from):
            #print("False, active player")
            return False

        valid_move = self.check_valid_move(moved_from, moved_to)
        if valid_move[0] is False:
            #print(valid_move, "= board move")
            return False
        self.update_game_board(moved_from, moved_to)
        self.check_for_captures(moved_to)
        self.corner_capture_check(moved_to)
        self.update_game_state()
        self.player_turn()

        print(self.print_board())
        print("Black captured=", self._black_captured)
        print("Red captured=", self._red_captured)
        print("Game state= ", self._game_state)
        print("Player turn= ", self._active_player)

    def check_valid_move(self, moved_from, moved_to):
        """
        This is a helper function to the 'make_move' function, it checks to see if the proposed move is a valid one by
        checking if it's a valid horizontal move, vertical move, and checks that it is only a horizontal or vertical
        move
        :return:
        """

        moved_from_tuple = self.convert_board_notation(moved_from)
        moved_to_tuple = self.convert_board_notation(moved_to)
        valid_move = [True]

        if moved_from_tuple[0] == moved_to_tuple[0]:  # checks for non-horizontal or vertical moves
            pass
        elif moved_from_tuple[1] == moved_to_tuple[1]:
            pass
        else:
            valid_move[0] = False
            valid_move.append("not valid direction")
            return valid_move

        if moved_from_tuple[0] == moved_to_tuple[0]:    # checks to see if it's a horizontal move, using rows
            row = self._game_board[moved_from_tuple[0]]
            if moved_from_tuple[1] > moved_to_tuple[1]:
                row = row[moved_to_tuple[1]:moved_from_tuple[1]]
            else:
                row = row[moved_from_tuple[1] + 1:moved_to_tuple[1] + 1]

            for board_space in row:
                if board_space == ".":
                    pass
                else:
                    valid_move[0] = False
                    valid_move.append("occupied space, row")
                    return valid_move
                return valid_move

        if moved_from_tuple[1] == moved_to_tuple[1]:    # for a vertical  move
            game_board_columns = self.game_board_columns()
            column = game_board_columns[moved_from_tuple[1]]
            if moved_from_tuple[0] > moved_to_tuple[0]:
                column = column[moved_to_tuple[0]:moved_from_tuple[0]]
            else:
                column = column[moved_from_tuple[0] + 1:moved_to_tuple[0] + 1]
            for board_space in column:
                if board_space == ".":
                    pass
                else:
                    valid_move[0] = False
                    valid_move.append("occupied space, column")
                    return valid_move
            return valid_move

    def check_for_captures(self, moved_to):
        """
        After a valid move has occurred, this checks for any valid captures, removes captured pieces and updates the
        number of each color captured pieces
        :param moved_to:
        :return:
        """

        moved_to_tuple = self.convert_board_notation(moved_to)
        square = self.get_square_occupant(moved_to)

        if square == "RED":               # checking to the left for captures
            captured_squares = 0
            for space in range(1, 9):
                if moved_to_tuple[1] - space < 0:
                    break
                if self._game_board[moved_to_tuple[0]][moved_to_tuple[1] - space] == "B":
                    captured_squares += 1
                elif self._game_board[moved_to_tuple[0]][moved_to_tuple[1] - space] == "R":
                    if captured_squares == 0:
                        break
                    if captured_squares == 1:
                        self._game_board[moved_to_tuple[0]][moved_to_tuple[1] - 1] = "."
                        self._black_captured += 1
                        break
                    for captured in range(1, captured_squares + 1):
                        self._game_board[moved_to_tuple[0]][moved_to_tuple[1] - captured] = "."
                        self._black_captured += 1
                    break
                else:
                    break

        if square == "RED":                      # checking to the right for captures
            captured_squares = 0
            for space in range(1, 9):
                if moved_to_tuple[1] == 8:
                    break
                if moved_to_tuple[1] + space == 9:
                    break
                if self._game_board[moved_to_tuple[0]][moved_to_tuple[1] + space] == "B":
                    captured_squares += 1
                elif self._game_board[moved_to_tuple[0]][moved_to_tuple[1] + space] == "R":
                    if captured_squares == 0:
                        break
                    if captured_squares == 1:
                        self._game_board[moved_to_tuple[0]][moved_to_tuple[1] + 1] = "."
                        self._black_captured += 1
                        break
                    for captured in range(1, captured_squares + 1):
                        self._game_board[moved_to_tuple[0]][moved_to_tuple[1] + captured] = "."
                        self._black_captured += 1
                    break
                else:
                    break

        if square == "RED":               # checking above for captures
            captured_squares = 0
            game_board_columns = self.game_board_columns()       # converts the board into columns with helper function
            for space in range(1, 9):
                if moved_to_tuple[0] == 0:
                    break
                if space != 1:
                    if moved_to_tuple[1] - space < 0:
                        break
                if moved_to_tuple[0] <= 1:
                    break
                if game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] - space] == "B":
                    captured_squares += 1
                elif game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] - space] == "R":
                    if captured_squares == 0:
                        break
                    if captured_squares == 1:
                        game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] - 1] = "."
                        self._black_captured += 1
                        game_board = self.game_board_rows(game_board_columns)
                        self._game_board = game_board
                        break
                    for captured in range(1, captured_squares + 1):
                        game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] - captured] = "."
                        self._black_captured += 1
                    game_board = self.game_board_rows(game_board_columns)
                    self._game_board = game_board
                    break
                else:
                    break

        if square == "RED":               # checking below for captures
            captured_squares = 0
            game_board_columns = self.game_board_columns()       # converts the board into columns with helper function
            for space in range(0, 9):
                if moved_to_tuple[0] >= 7:
                    break
                if moved_to_tuple[0] + space == 9:
                    break
                if game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] + space] == "B":
                    captured_squares += 1
                elif game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] + space] == "R":
                    if captured_squares == 0:
                        break
                    if captured_squares == 1:
                        game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] + 1] = "."
                        self._black_captured += 1
                        game_board = self.game_board_rows(game_board_columns)
                        self._game_board = game_board
                        break
                    for captured in range(1, captured_squares + 1):
                        game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] + captured] = "."
                        self._black_captured += 1
                    game_board = self.game_board_rows(game_board_columns)
                    self._game_board = game_board
                    break
                else:
                    break

        if square == "BLACK":  # checking to the left for captures
            captured_squares = 0
            for space in range(1, 9):
                if moved_to_tuple[1] - space < 0:
                    break
                if self._game_board[moved_to_tuple[0]][moved_to_tuple[1] - space] == "R":
                    captured_squares += 1
                elif self._game_board[moved_to_tuple[0]][moved_to_tuple[1] - space] == "B":
                    if captured_squares == 0:
                        break
                    if captured_squares == 1:
                        self._game_board[moved_to_tuple[0]][moved_to_tuple[1] - 1] = "."
                        self._red_captured += 1
                        break
                    for captured in range(1, captured_squares + 1):
                        self._game_board[moved_to_tuple[0]][moved_to_tuple[1] - captured] = "."
                        self._red_captured += 1
                    break
                else:
                    break

        if square == "BLACK":  # checking to the right for captures
            captured_squares = 0
            for space in range(1, 9):
                if moved_to_tuple[1] == 8:
                    break
                if moved_to_tuple[1] + space == 9:
                    break
                if self._game_board[moved_to_tuple[0]][moved_to_tuple[1] + space] == "R":
                    captured_squares += 1
                elif self._game_board[moved_to_tuple[0]][moved_to_tuple[1] + space] == "B":
                    if captured_squares == 0:
                        break
                    if captured_squares == 1:
                        self._game_board[moved_to_tuple[0]][moved_to_tuple[1] + 1] = "."
                        self._red_captured += 1
                        break
                    for captured in range(1, captured_squares + 1):
                        self._game_board[moved_to_tuple[0]][moved_to_tuple[1] + captured] = "."
                        self._red_captured += 1
                    break
                else:
                    break

        if square == "BLACK":  # checking above for captures
            captured_squares = 0
            game_board_columns = self.game_board_columns()  # converts the board into columns with helper function
            for space in range(1, 9):
                if moved_to_tuple[0] == 0:
                    break
                if space != 1:
                    if moved_to_tuple[1] - space < 0:
                        break
                if moved_to_tuple[0] <= 1:
                    break
                if game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] - space] == "R":
                    captured_squares += 1
                elif game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] - space] == "B":
                    if captured_squares == 0:
                        break
                    if captured_squares == 1:
                        game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] - 1] = "."
                        self._red_captured += 1
                        game_board = self.game_board_rows(game_board_columns)
                        self._game_board = game_board
                        break
                    for captured in range(1, captured_squares + 1):
                        game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] - captured] = "."
                        self._red_captured += 1
                    game_board = self.game_board_rows(game_board_columns)
                    self._game_board = game_board
                    break
                else:
                    break

        if square == "BLACK":  # checking below for captures
            captured_squares = 0
            game_board_columns = self.game_board_columns()  # converts the board into columns with helper function
            for space in range(1, 8):
                if moved_to_tuple[0] >= 7:
                    break
                if moved_to_tuple[0] + space == 9:
                    break
                if game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] + space] == "R":
                    captured_squares += 1
                elif game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] + space] == "B":
                    if captured_squares == 0:
                        break
                    if captured_squares == 1:
                        game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] + 1] = "."
                        self._red_captured += 1
                        game_board = self.game_board_rows(game_board_columns)
                        self._game_board = game_board
                        break
                    for captured in range(1, captured_squares + 1):
                        game_board_columns[moved_to_tuple[1]][moved_to_tuple[0] + captured] = "."
                        self._red_captured += 1
                    game_board = self.game_board_rows(game_board_columns)
                    self._game_board = game_board
                    break
                else:
                    break

    def player_turn(self):
        """
        This is a simple helper function that updates who's current turn it is, after a valid move.
        :return:
        """

        whose_turn = self._active_player

        if whose_turn == "RED":
            self._active_player = "BLACK"

        else:
            self._active_player = "RED"

    def update_game_board(self, moved_from, moved_to):
        """
        This is a helper function that after a move has been validated it will move the requested piece and update the
        game board.
        :param moved_from:
        :param moved_to:
        :return:
        """

        moved_from_tuple = self.convert_board_notation(moved_from)
        moved_to_tuple = self.convert_board_notation(moved_to)
        game_board = self._game_board
        game_board[moved_to_tuple[0]][moved_to_tuple[1]] = game_board[moved_from_tuple[0]][moved_from_tuple[1]]
        game_board[moved_from_tuple[0]][moved_from_tuple[1]] = "."

        self._game_board = game_board

    def corner_capture_check(self, moved_to):
        """
        This is a helper function to the 'remove_piece' function, to check for the special situation for corner captures
        :param moved_to:
        :return:
        """
        moved_to_tuple = self.convert_board_notation(moved_to)
        square = self.get_square_occupant(moved_to)

        if square == "RED":
            if moved_to_tuple == (1, 0):           # checking upper left corner
                if self._game_board[0][0] == "B":
                    if self._game_board[0][1] == "R":
                        self._game_board[0][0] = "."
                        self._black_captured += 1
            if moved_to_tuple == (0, 1):           # checking upper left corner
                if self._game_board[0][0] == "B":
                    if self._game_board[1][0] == "R":
                        self._game_board[0][0] = "."
                        self._black_captured += 1
            if moved_to_tuple == (0, 7):           # checking upper right corner
                if self._game_board[0][8] == "B":
                    if self._game_board[1][8] == "R":
                        self._game_board[0][8] = "."
                        self._black_captured += 1
            if moved_to_tuple == (1, 8):           # checking upper right corner
                if self._game_board[0][8] == "B":
                    if self._game_board[0][7] == "R":
                        self._game_board[0][8] = "."
                        self._black_captured += 1
            if moved_to_tuple == (7, 8):           # checking lower right corner
                if self._game_board[8][8] == "B":
                    if self._game_board[8][7] == "R":
                        self._game_board[8][8] = "."
                        self._black_captured += 1
            if moved_to_tuple == (8, 7):           # checking lower right corner
                if self._game_board[8][8] == "B":
                    if self._game_board[7][8] == "R":
                        self._game_board[8][8] = "."
                        self._black_captured += 1
            if moved_to_tuple == (8, 1):           # checking lower left corner
                if self._game_board[8][0] == "B":
                    if self._game_board[7][0] == "R":
                        self._game_board[8][0] = "."
                        self._black_captured += 1
            if moved_to_tuple == (7, 0):           # checking lower left corner
                if self._game_board[8][0] == "B":
                    if self._game_board[8][1] == "R":
                        self._game_board[8][0] = "."
                        self._black_captured += 1

        if square == "BLACK":
            if moved_to_tuple == (1, 0):           # checking upper left corner
                if self._game_board[0][0] == "R":
                    if self._game_board[0][1] == "B":
                        self._game_board[0][0] = "."
                        self._red_captured += 1
            if moved_to_tuple == (0, 1):           # checking upper left corner
                if self._game_board[0][0] == "R":
                    if self._game_board[1][0] == "B":
                        self._game_board[0][0] = "."
                        self._red_captured += 1
            if moved_to_tuple == (0, 7):           # checking upper right corner
                if self._game_board[0][8] == "R":
                    if self._game_board[1][8] == "B":
                        self._game_board[0][8] = "."
                        self._red_captured += 1
            if moved_to_tuple == (1, 8):           # checking upper right corner
                if self._game_board[0][8] == "R":
                    if self._game_board[0][7] == "B":
                        self._game_board[0][8] = "."
                        self._red_captured += 1
            if moved_to_tuple == (7, 8):           # checking lower right corner
                if self._game_board[8][8] == "R":
                    if self._game_board[8][7] == "B":
                        self._game_board[8][8] = "."
                        self._red_captured += 1
            if moved_to_tuple == (8, 7):           # checking lower right corner
                if self._game_board[8][8] == "R":
                    if self._game_board[7][8] == "B":
                        self._game_board[8][8] = "."
                        self._red_captured += 1
            if moved_to_tuple == (8, 1):           # checking lower left corner
                if self._game_board[8][0] == "R":
                    if self._game_board[7][0] == "B":
                        self._game_board[8][0] = "."
                        self._red_captured += 1
            if moved_to_tuple == (7, 0):           # checking lower left corner
                if self._game_board[8][0] == "R":
                    if self._game_board[8][1] == "B":
                        self._game_board[8][0] = "."
                        self._red_captured += 1

    def game_board_columns(self):
        """
        This re-formats the game board into lists of columns instead of rows, for valid moves and piece capture checks,
        for vertical moves. Just like 'game_board' this is a list of lists, where each list is a column. The list of
        lists is labeled 'game_board_columns' This is a helper function for make_move, check_valid_move and
        remove_pieces
        :return:
        """

        game_board_columns = []
        board_range = range(9)

        for board_column in board_range:
            column = []
            for column_space in board_range:
                board_space = self._game_board[column_space][board_column]
                column.append(board_space)
            game_board_columns.append(column)

        return game_board_columns

    def game_board_rows(self, game_board_columns):
        """
        This is a helper function for check_for_capture function. This takes the game board that has been turned into
        columns from the game_board_columns function, and turns it back into rows, how it is original set up in the
        class
        :return:
        """

        game_board_row = []
        board_range = range(9)

        for board_column in board_range:
            column = []
            for column_space in board_range:
                board_space = game_board_columns[column_space][board_column]
                column.append(board_space)
            game_board_row.append(column)

        return game_board_row

    def print_board(self):
        """
        This is mainly for testing purposes, returns and prints the current board
        :return:
        """
        board = self._game_board
        separator = " "

        print("  1 2 3 4 5 6 7 8 9 ")
        print("a", separator.join(board[0]))
        print("b", separator.join(board[1]))
        print("c", separator.join(board[2]))
        print("d", separator.join(board[3]))
        print("e", separator.join(board[4]))
        print("f", separator.join(board[5]))
        print("g", separator.join(board[6]))
        print("h", separator.join(board[7]))
        print("i", separator.join(board[8]))


#game = HasamiShogiGame()
#game.print_board()
#game.make_move("i8", "g8")
#print(game.get_active_player())
#game.make_move("a9", "h9")
#game.make_move("g8", "g9")
#game.make_move("b2", "b3")
#game.make_move("i2", "a2")
#game.make_move("b3", "b4")
#game.make_move("c1", "b1")
#game.make_move("d1", "d2")
#game.make_move("i6", "f6")
#game.make_move("a1", "a2")

#print(game.get_game_state())
#print(game.get_active_player())
#print("BLACK =", game.get_num_captured_pieces("BLACK"))
#print("RED =", game.get_num_captured_pieces("RED"))

