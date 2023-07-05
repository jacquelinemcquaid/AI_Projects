# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import random
import numpy as np
from copy import deepcopy


@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A class to implement a student agent using an AI approach.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Returns the next best step.

        Parameters
        ----------
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        my_pos : tuple (x,y)
            The position of the student.
        adv_pos: tuple (x,y)
            The position of the opponent.
        max_step: integer
            The maximum step the agent can take on the board
        """

        # Determining if we can move to the opponent and box it in
        position, direction = self.boxPlayerIn(chess_board, my_pos, adv_pos)

        # If the direction doesn't equal "None", then it is possible to block it in and win the game
        if direction != None:

            # Returning the position and direction
            return position, direction

        # Otherwise, we use a Monte Carlo Tree Search approach to simulate random games
        else:

            # Finding the limits of the next possible x and y values of my_pos
            if (my_pos[0] - max_step < 0):
                lowerLimitx = 0
            else:
                lowerLimitx = my_pos[0] - max_step
            if (my_pos[0] + max_step > len(chess_board)):
                upperLimitx = len(chess_board)
            else:
                upperLimitx = my_pos[0] + max_step
            if my_pos[1] - max_step < 0:
                lowerLimity = 0
            else:
                lowerLimity = my_pos[1] - max_step
            if my_pos[1] + max_step > len(chess_board):
                upperLimity = len(chess_board)
            else:
                upperLimity = my_pos[1] + max_step

            # Findng a random child (possible next step)
            position, dir = self.createRandomChild(lowerLimitx, upperLimitx, lowerLimity, upperLimity, my_pos,
                                                   chess_board, adv_pos)

            # Creating a position of the correct form for our simulation function
            listPos = [position, 0, dir, 0]

            # Keeping track of the wins of each simulated child, the simulation count per round,
            # and the total simulation count
            wins = 0
            countSimulations = 0
            totalCount = 0

            # Best position holds the position, direction, and score
            bestPositionBestWin = [(0, 0), 0, 0]

            # Running 20 simulations
            while countSimulations <= 20:

                # Calculating if we win or lose (+1 for win, 0 for lose)
                score = self.randomSimulations(listPos, adv_pos, max_step, chess_board)

                # Adding to the wins count
                wins += score

                # Checking our wins after 5 simulations
                if countSimulations == 5:
                    # If we haven't won any games after 5 simulations, trying a new child
                    if wins == 0:
                        # Finding a random child (possible next step)
                        position, dir = self.createRandomChild(lowerLimitx, upperLimitx, lowerLimity, upperLimity,
                                                               my_pos, chess_board, adv_pos)

                        # Resetting the position, wins count, and simulation count for a given child
                        listPos = [position, 0, dir, 0]
                        wins = 0
                        countSimulations = 0

                        continue

                # Checking our wins after 10 simulations
                if countSimulations == 10:
                    # If we have one less than 50% of the games, trying a new child
                    if wins / 10 < 0.5:
                        # Finding a random child (possible next step)
                        position, dir = self.createRandomChild(lowerLimitx, upperLimitx, lowerLimity, upperLimity,
                                                               my_pos, chess_board, adv_pos)

                        # Resetting the position, wins count, and simulation count for a given child
                        listPos = [position, 0, dir, 0]
                        wins = 0
                        countSimulations = 0
                        continue

                # Incrementing the simulation count
                countSimulations += 1
                totalCount += 1

                # If we reach 20 simulations
                if countSimulations == 20:
                    # If we win 15/20 games or more, returning the position and the barrier to be played next
                    if wins / 20 >= 0.75:

                        return listPos[0], listPos[2]

                    # Otherwise, we have to try a random move
                    else:
                        # In case we run out of time to check more children, keeping track of
                        # the best next move so far
                        if wins > bestPositionBestWin[1]:
                            bestPositionBestWin[0] = position
                            bestPositionBestWin[1] = listPos[2]
                            bestPositionBestWin[2] = wins

                        # Before we start simulating again, we have to make sure we are within the time limit
                        # by checking the total simulation count. If we have done too many simulations, we return
                        # the best child so far

                        # If the length of the board is 9, we don't want to do more than
                        # 500 simulations
                        if len(chess_board) == 9 and totalCount >= 500:
                            return bestPositionBestWin[0], bestPositionBestWin[1]

                        # If the length of the board is 8, we don't want to do more than
                        # 600 simulations
                        if len(chess_board) == 8 and totalCount >= 600:
                            return bestPositionBestWin[0], bestPositionBestWin[1]

                        # If the length of the board is 7, we don't want to do more than
                        # 700 simulations
                        if len(chess_board) == 7 and totalCount >= 700:
                            return bestPositionBestWin[0], bestPositionBestWin[1]

                        # If the length of the board is 6, we don't want to do more than 800
                        # simulations
                        if len(chess_board) == 6 and totalCount >= 800:
                            return bestPositionBestWin[0], bestPositionBestWin[1]

                        # If the length of the board is 5, we don't want to do more than
                        # 1000 simulations
                        if len(chess_board) == 5 and totalCount >= 1000:
                            return bestPositionBestWin[0], bestPositionBestWin[1]

                        # Finding a random child (possible next step)
                        position, dir = self.createRandomChild(lowerLimitx, upperLimitx, lowerLimity, upperLimity,
                                                               my_pos, chess_board, adv_pos)

                        # Resetting the position, wins count, and simulation count of the last child
                        listPos = [position, 0, dir, 0]
                        wins = 0
                        countSimulations = 0

    # Helper function to create a random child
    # Takes as input the lower and upper limits of x and y based on the max step, the students position, the
    # chessboard, and the opponents position.
    # Returns a random valid child (possible next move)
    def createRandomChild(self, lowerLimitx, upperLimitx, lowerLimity, upperLimity, my_pos, chess_board, adv_pos):
        """
        Returns a random valid next move within the specified parameters

        Parameters
        ----------
        lowerLimitx: integer
            The lower limit of the possible move on the x-axis of the chessboard
        upperLimitx: integer
            The upper limit of the possible move on the x-axis of the chessboard
        lowerLimity: integer
            The lower limit of the possible move on the y-axis of the chessboard
        upperLimity: integer
            The upper limit of the possible move on the y-axis of the chessboard
        my_pos : tuple (x,y)
            The position of the student.
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        adv_pos: tuple (x,y)
            The position of the opponent.
        """

        # Creating a random x with the limits
        x = random.randint(lowerLimitx, upperLimitx)

        # Creating a random y with the limits
        y = random.randint(lowerLimity, upperLimity)

        # Creating the position tuple
        position = (x, y)

        # Creating a deep copy of the position to check validity
        position2 = deepcopy(position)

        # Creating a random border
        dir = random.randint(0, 3)

        # Creating a new random position until one is valid
        while (self.check_valid_step(my_pos, np.asarray(position2), dir, chess_board, adv_pos) == False):
            # Creating a random x with the limits
            x = random.randint(lowerLimitx, upperLimitx)

            # Creating a random y with the limits
            y = random.randint(lowerLimity, upperLimity)

            position = (x, y)
            position2 = deepcopy(position)
            dir = random.randint(0, 3)

        return position, dir

    # Takes as input the chessboard, the students position, and the opponents position
    # Returns the position and direction of border if the student is able to box the opponent in
    # Otherwise, it returns None
    def boxPlayerIn(self, chess_board, my_pos, adv_pos):
        """
        Check if it's possible to box the opponent in and win the game

        Parameters
        ----------
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        my_pos : tuple (x,y)
            The position of the student.
        adv_pos: tuple (x,y)
            The position of the opponent.
        """

        # Check if there are three barriers at the opponents position
        if self.numberOfBorders(chess_board, adv_pos) == 3:

            # Finding the direction of the location with no border
            # There should only be one location with no border

            for i in range(0, 4):
                if chess_board[adv_pos[0], adv_pos[1], i] == False:
                    borderDirection = i

            # If the direction with no border is up, the student must be one cell above the opponent
            if borderDirection == 0:
                x = adv_pos[0] - 1
                y = adv_pos[1]

                blockPosition = (x, y)
                nextPosition = np.asarray(blockPosition)

                # The direction to block would be down if the student blocks from above
                directionToBlock = 2

                # Checking if the move is valid
                valid = self.check_valid_step(my_pos, nextPosition, directionToBlock, chess_board, adv_pos)

                if valid:
                    return blockPosition, directionToBlock

            # The direction with no border is right
            elif borderDirection == 1:

                # The empty border is to the right, therefore the student must be one cell to the right
                # And must place a border to the left

                x = adv_pos[0]
                y = adv_pos[1] + 1

                blockPosition = (x, y)
                nextPosition = np.asarray(blockPosition)

                # The direction to block would be left
                directionToBlock = 3

                # Checking if the move is valid
                valid = self.check_valid_step(my_pos, nextPosition, directionToBlock, chess_board, adv_pos)

                if valid:
                    return blockPosition, directionToBlock

            # The empty border is down
            elif borderDirection == 2:

                # The empty border is down, therefore the student must be one cell under the opponent and
                # place a border in direction up

                x = adv_pos[0] + 1
                y = adv_pos[1]

                blockPosition = (x, y)
                nextPosition = np.asarray(blockPosition)

                # The direction to block would be down
                directionToBlock = 0

                # Checking if the move is valid
                valid = self.check_valid_step(my_pos, nextPosition, directionToBlock, chess_board, adv_pos)

                if valid:
                    return blockPosition, directionToBlock

            # The empty border is left
            elif borderDirection == 3:

                # The empty border is left, therefore the student must be one cell to the right of the opponent
                # and place a border to the right

                x = adv_pos[0]
                y = adv_pos[1] - 1

                blockPosition = (x, y)
                nextPosition = np.asarray(blockPosition)

                # The direction to block would be down
                directionToBlock = 1

                # Checking if the move is valid
                valid = self.check_valid_step(my_pos, nextPosition, directionToBlock, chess_board, adv_pos)

                if valid:
                    return blockPosition, directionToBlock

        # If we reach this point, there are no valid moves
        return (None, None), None

    def check_endgame(self, board_size, chess_board, my_pos, adv_pos):
        """
        Check if the game ends and compute the current score of the agents.
        Returns a boolean is_endgame determining if the game ends, my_pos score, and adv_pos score

        Parameters
        ----------
        board_size: int
            The size of the baord
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        my_pos : tuple (x,y)
            The position of the student.
        adv_pos: tuple (x,y)
            The position of the opponent.
        """

        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

        # Union-Find
        father = dict()
        for r in range(board_size):
            for c in range(board_size):
                father[(r, c)] = (r, c)

        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]

        def union(pos1, pos2):
            father[pos1] = pos2

        for r in range(board_size):
            for c in range(board_size):
                for dir, move in enumerate(
                        moves[1:3]
                ):  # Only check down and right
                    if chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)

        for r in range(board_size):
            for c in range(board_size):
                find((r, c))
        p0_r = find(tuple(my_pos))
        p1_r = find(tuple(adv_pos))
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        if p0_r == p1_r:
            return False, p0_score, p1_score
        player_win = None
        win_blocks = -1
        if p0_score > p1_score:
            player_win = 0
            win_blocks = p0_score
        elif p0_score < p1_score:
            player_win = 1
            win_blocks = p1_score
        else:
            player_win = -1  # Tie

        # p0 is student position, p1 is random position
        return True, p0_score, p1_score

    # Takes as input a position and the board size. If the position is within the boundaries, returns True
    # Otherwise, returns False
    def check_boundary(self, pos, board_size):
        """
        Checks if the position is within the boundary of the baord

        Parameters
        ----------
        pos: tuple (x, y)
            Position
        board_size: int
            The size of the baord

        """

        # The row and column values of the position
        r, c = pos
        return 0 <= r < board_size and 0 <= c < board_size

    # Takes as input the current position of the player, and the next move, one step to the left, right, down, or up
    # Returns true if move is valid (does not cross borders) and false otherwise
    def validMove(self, chessboard, position1, position2):
        """
        Checks if the move from position1 to position2 is valid
        Returns True if the move is valid, False otherwise

        Parameters
         ----------
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        position1 : tuple (x,y)
            The current position
        position2: tuple (x,y)
            The next position to check validity
        """

        # Check if the new position is in the chessboard range and the new position is not the
        # same as the opponent position
        if self.check_boundary(position2, len(chessboard)) and position1 != position2:

            # Finding the coordinates of the x and y initial positions
            xPosition1 = position1[0]
            yPosition1 = position1[1]

            xPosition2 = position2[0]
            yPosition2 = position2[1]

            # Moving in the y direction
            if xPosition2 - xPosition1 == 0:
                # Moving one position left
                if yPosition2 - yPosition1 > 0:
                    # checking right border of position 2
                    if not chessboard[position2[0], position2[1], 3]:
                        return True
                # Moving one position to the right
                else:
                    # checking the left border of position 2
                    if not chessboard[position2[0], position2[1], 1]:
                        return True
            # moving in the y direction
            else:
                # Moving up
                if xPosition2 - xPosition1 > 0:
                    if not chessboard[position2[0], position2[1], 0]:
                        return True
                # Moving down
                else:
                    if not chessboard[position2[0], position2[1], 2]:
                        return True

        # Otherwise, the move is not valid
        return False

    # Checks if the step is valid
    def check_valid_step(self, start_pos, end_pos, barrier_dir, chess_board, opponent):
        """
        Check if the step the agent takes is valid (reachable and within max steps).

        Parameters
        ----------
        start_pos : tuple (x, y)
            The start position of the agent.
        end_pos : np.ndarray
            The end position of the agent.
        barrier_dir : int
            The direction of the barrier.
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        opponent : tuple (x, y)
            The opponents position
        """

        # Checking if there is a boundary
        if self.check_boundary(end_pos, len(chess_board)) == False:
            return False

        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

        max_step = (len(chess_board) + 1) // 2

        # Endpoint already has barrier or is boarder
        r, c = end_pos
        if chess_board[r, c, barrier_dir]:
            return False
        if np.array_equal(start_pos, end_pos):
            return True

        # Get position of the adversary
        adv_pos = opponent

        # BFS
        state_queue = [(start_pos, 0)]
        visited = {tuple(start_pos)}
        is_reached = False
        while state_queue and not is_reached:
            cur_pos, cur_step = state_queue.pop(0)
            # print("The current position: " + str(cur_pos))
            r, c = cur_pos
            if cur_step == max_step:
                break
            for dir, move in enumerate(moves):
                if chess_board[r, c, dir]:
                    continue

                next_pos = (cur_pos[0] + move[0], cur_pos[1] + move[1])
                if np.array_equal(next_pos, adv_pos) or tuple(next_pos) in visited:
                    continue
                if np.array_equal(next_pos, end_pos):
                    is_reached = True
                    break

                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))

        return is_reached

    def randomSimulations(self, totalPosition, adv_pos, max_step, chess_board):
        """
        Runs random simulations of the game.
        Returns +1 if the student wins or if there is a tie, and negative 0 if the opponent wins

        Parameters
        ----------
        totalPosition: An array of the form [(x, y), direction, score]
            The current position, direction, and score of the student
        adv_pos: tuple (x, y)
            Opponent position
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        """

        # Declaring the position and direction of the next move
        my_pos = totalPosition[0]
        dir = totalPosition[2]

        copyChessboard = deepcopy(chess_board)
        copyMyPos = deepcopy(my_pos)
        copyAdvPos = deepcopy(adv_pos)
        copyDir = deepcopy(dir)

        # Moving to the new position and setting a barrier
        self.set_barrier(my_pos[0], my_pos[1], copyDir, copyChessboard)

        # Determining whether we reached the end of the game, and the scores of the student and the opponent
        endGame, myScore, opponentScore = self.check_endgame(len(copyChessboard), copyChessboard, copyMyPos, copyAdvPos)

        # Playing random moves and adding barriers to the chessboard until the game is over
        while (endGame == False):

            # Checking if the opponent can box the student in
            # boxPosition, boxDirection = self.boxPlayerIn(copyChessboard, copyAdvPos, copyMyPos)

            # Random move of the opponent
            newOpponentPosition, directionBarrierOpponent = self.random_walk(copyAdvPos, copyMyPos, max_step,
                                                                             copyChessboard)

            # Setting a random barrier
            self.set_barrier(newOpponentPosition[0], newOpponentPosition[1], directionBarrierOpponent, copyChessboard)

            # Setting the new opponent position
            copyAdvPos = newOpponentPosition

            # Checking if the game is over and calculating scores
            endGame, myScore, opponentScore = self.check_endgame(len(copyChessboard), copyChessboard, copyMyPos,
                                                                 copyAdvPos)

            if endGame:
                break

            # Random move of the student
            newStudentPosition, directionBarrierStudent = self.random_walk(copyMyPos, copyAdvPos, max_step,
                                                                           copyChessboard)

            # Setting the barrier
            self.set_barrier(newStudentPosition[0], newStudentPosition[1], directionBarrierStudent, copyChessboard)

            # Declaring the new random positions
            copyMyPos = newStudentPosition

            endGame, myScore, opponentScore = self.check_endgame(len(copyChessboard), copyChessboard, copyMyPos,
                                                                 copyAdvPos)

            if endGame:
                break

        # If the student score is greater than or equal to the opponents, we return true (student wins)
        if myScore >= opponentScore:
            return 1

        # Otherwise, return false
        else:
            return 0

    # Takes as input two players, returns a new random position of the first player input
    def random_walk(self, my_pos, adv_pos, max_step, chess_board):
        """
        Randomly walk to the next position in the board.

        Parameters
        ----------
        my_pos : tuple
            The position of the agent.
        adv_pos : tuple
            The position of the adversary.
        max_step: integer
            The maximum step the player can take
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        """
        ori_pos = deepcopy(my_pos)
        steps = np.random.randint(0, max_step + 1)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        # Random Walk
        for _ in range(steps):
            r, c = my_pos
            dir = np.random.randint(0, 4)
            m_r, m_c = moves[dir]
            my_pos = (r + m_r, c + m_c)

            # Special Case enclosed by Adversary
            k = 0
            while chess_board[r, c, dir] or (my_pos[0] == adv_pos[0] and my_pos[1] == adv_pos[1]):
                # print("While loop in random_walk")
                k += 1
                if k > 300:
                    break
                dir = np.random.randint(0, 4)
                m_r, m_c = moves[dir]
                my_pos = (r + m_r, c + m_c)

            if k > 300:
                my_pos = ori_pos
                break

        # Put Barrier
        dir = np.random.randint(0, 4)
        r, c = my_pos

        allBlocked = True
        for i in range(0, 4):
            if chess_board[r, c, i] == False:
                allBlocked = False

        if allBlocked:
            return None, None

        while chess_board[r, c, dir]:
            dir = np.random.randint(0, 4)

        return my_pos, dir

    # Takes as input the row, column, chessboard, and position to place the barier
    def set_barrier(self, r, c, dir, chess_board):
        """
        Set a barrier on the board

        Parameters
        ----------
        r: integer
            Row index
        c: integer
            Column index
        dir: integer
            The direction of the border
        chess_board : a numpy array of shape (x_max, y_max, 4)
                The chess_board of the game.
        """

        # Set the barrier to True
        chess_board[r, c, dir] = True
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        opposites = {0: 2, 1: 3, 2: 0, 3: 1}

        # Set the opposite barrier to True
        move = moves[dir]
        if r + move[0] < len(chess_board) and c + move[1] < len(chess_board):
            chess_board[r + move[0], c + move[1], opposites[dir]] = True

    # Takes as input the chessboard and the position
    # Returns the number of borders at the specified position
    def numberOfBorders(self, chessboard, position):
        """
        Determining the number of borders at a certain position
        Returns an integer representing the number of borders

        Parameters
        ----------
        chess_board : a numpy array of shape (x_max, y_max, 4)
            The chess_board of the game.
        position : tuple
            The position to check
                adv_pos : tuple
        """

        x = position[0]
        y = position[1]

        count = 0

        for i in range(0, 4):
            if chessboard[x, y, i] == True:
                count += 1

        return count