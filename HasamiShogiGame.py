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

        #checks for valid input
        valid_input = self.check_valid_input(moved_from, moved_to)
        if valid_input is False:
            return False
        #checks for valid move
        valid_move = self.check_valid_move(moved_from, moved_to)
        if valid_move is False:
            return False
        
        self.update_game_board(moved_from, moved_to)
        self.check_for_captures(moved_to)
        self.corner_capture_check(moved_to)
        self.update_game_state()
        self.player_turn()

    def check_valid_input(self, moved_from, moved_to):
        """
        This function checks to make sure that the inputs from moved_from and moved_to are valid moves for the game board
        """

        #check valid input lengths
        if len(moved_from) != 2:
            return False             
        if len(moved_to) != 2:
            return False
        

        valid_letters = "abcdefghi"
        valid_numbers = "123456789"

        from_row = moved_from[0]
        from_col = moved_from[1]
        to_row = moved_to[0]
        to_col = moved_to[1]

        #checking for valid letter/row from moved_from (selected_piece)
        #initialize loop
        test_answer = False
        for letter in valid_letters:
            if letter == from_row:
                test_answer = True
        #updating after loop
        if test_answer == False:
            return False
        
        #checking for valid number/column from moved_from (selected_piece)
        test_answer = False
        for num in valid_numbers:
            if num == from_col:
                test_answer = True
        #updating after loop
        if test_answer == False:
            return False
        
        #checking for valid letter/row from moved_to (move_to)
        #initialize loop
        test_answer = False
        for letter in valid_letters:
            if letter == to_row:
                test_answer = True
        #updating after loop
        if test_answer == False:
            return False       

        #checking for valid number/column from moved_to (move_to)
        test_answer = False
        for num in valid_numbers:
            if num == to_col:
                test_answer = True
        #updating after loop
        if test_answer == False:
            return False
        
        #if no test returns False, then return True
        return True
 
    def check_valid_move(self, moved_from, moved_to):
        """
        This is a helper function to the 'make_move' function, it checks to see if the proposed move is a valid one by
        checking if it's a valid horizontal move, vertical move, and checks that it is only a horizontal or vertical
        move
        :return:
        """

        if moved_from == moved_to:
            return False
        
        moved_from_tuple = self.convert_board_notation(moved_from)
        moved_to_tuple = self.convert_board_notation(moved_to)
        valid_move = [True]

        # checks for non-horizontal or vertical moves
        if moved_from_tuple[0] == moved_to_tuple[0]:
            pass
        elif moved_from_tuple[1] == moved_to_tuple[1]:
            pass
        else:
            valid_move[0] = False
            valid_move.append("not valid direction")
            return valid_move

        # checks to see if it's a horizontal move, using rows
        if moved_from_tuple[0] == moved_to_tuple[0]:    
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

        # for a vertical  move
        if moved_from_tuple[1] == moved_to_tuple[1]:    
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

    #BLACK Captures
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

    #RED Captures
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

    def play_game(self):
        """
        This is a helper function that does all the behind the scene function calls, to make the game easy to play for the user.
        """
        print("Game state= ", self.get_game_state())
        print("Black captured=", self.get_num_captured_pieces("BLACK"))
        print("Red captured=", self.get_num_captured_pieces("RED"))
        game.print_board()
        print("\nPlayer's turn:", game.get_active_player())
        selected_piece = input("Select Piece:")
        move_to = input("Move to:")
        print("\n")

        check_input = game.check_valid_input(selected_piece, move_to)
        if check_input == False:
            print("**** INVALID INPUT! a1 --> i9 ONLY ****\n")
            return

        check_move = game.make_move(selected_piece, move_to)
        if check_move == False:
            print("#### INVALID MOVE! TRY AGAIN ####\n")


if __name__ == "__main__":
    print(
        """
\n************************************************************************************************************************\n
                    Hello and Welcome to the Hasami Shogi Game! (Variant 1)\n
Hasami Shogi is a game played on a board similar to chess or checkers. There are two players, where one
controls the Red pieces 'R', and the other the Black pieces 'B'. The point of the game is to capture all
or all but one of your opponents pieces.

Game Play
The game begins with the player controlling the Black pieces. On your turn you can move any one piece
veritcal or horizontal on the game board (similar to a rook in chess). You cannot move through other pieces.
Use algebraic coordinates to move, for example (i1, b1) Only valid lowercase letter/number pairs are valid.

Play passes back and forth until the game is over (when one player has 0 or 1 pieces left).

Capturing pieces
Similar to 'Go' you can capture one or more pieces by having one of your pieces on each side of an opponent's 
piece(s), either horizontally or vertically. You may also capture a corner piece by being on the space above 
or below it and the other on one side or the other (see the following diagram for example)

(Imagine this is the upper left corner)
B R _ _ _
R _ _ _ _

Red would capture black's piece.

************************************************************************************************************************\n
"""
    )
    game = HasamiShogiGame()
    while game._game_state == "UNFINISHED":
        game.play_game()

    print("Game state= ", game.get_game_state())
    print("Black captured=", game.get_num_captured_pieces("BLACK"))
    print("Red captured=", game.get_num_captured_pieces("RED"))
    game.print_board()
    print("Game state= ", game.get_game_state(),"\n")
