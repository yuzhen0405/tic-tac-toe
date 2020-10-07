# coding: UTF-8
import random


class Minimax(object):
    board = None
    color = ['O', 'X']

    def __init__(self, board):
        self.board = board

    def bestMove(self, depth, state, curr_player):

        if curr_player == self.color[0]:
            opp_player = self.color[1]
        else:
            opp_player = self.color[0]

        # enumerate all legal moves
        legal_moves = {}  # will map legal move states to their alpha values
        for i in range(9):
            # if i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in i for curr_player
                temp = self.makeMove(state, i, curr_player)
                # legal_moves[key] = value            #temp=the board with added move
                legal_moves[i] = -self.search(depth - 1, temp, opp_player)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def search(self, depth, state, curr_player):
        """ Searches the tree at depth 'depth'
            By default, the state is the board, and curr_player is whomever 
            called this search
            
            Returns the alpha value
        """

        # enumerate all legal moves from this state
        legal_moves = []  # list
        for i in range(9):
            # if column i is a legal move...
            if self.isLegalMove(i, state):
                # make the move in column i for curr_player
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # if this node (state) is a terminal node or depth == 0...
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            # return the heuristic value of node
            return self.value(state, curr_player)

        # determine opponent's color
        if curr_player == self.color[0]:
            opp_player = self.color[1]
        else:
            opp_player = self.color[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth - 1, child, opp_player))
        return alpha

    def isLegalMove(self, i, state):
        """ Boolean function to check if a move (column) is a legal move
        """
        if state[i] == '-':
            # once we find the first empty, we know it's a legal move
            return True
        # if we get here, the column is full
        return False

    def gameIsOver(self, state):
        if self.checkForStreak(state, self.color[0], 3) >= 1:
            return True
        elif self.checkForStreak(state, self.color[1], 3) >= 1:
            return True
        else:
            return False

    def makeMove(self, state, i, color):
        """ Change a state object to reflect a player, denoted by color,
            making a move at column 'column'
            
            Returns a copy of new state array with the added move
        """

        temp = [x[:] for x in state]
        if temp[i] == '-':
            temp[i] = color
            return temp

    def value(self, state, color):
        """ Simple heuristic to evaluate board configurations
            Heuristic is (num of 4-in-a-rows)*99999 + (num of 3-in-a-rows)*100 + 
            (num of 2-in-a-rows)*10 - (num of opponent 4-in-a-rows)*99999 - (num of opponent
            3-in-a-rows)*100 - (num of opponent 2-in-a-rows)*10
        """
        if color == self.color[0]:
            o_color = self.color[1]
        else:
            o_color = self.color[0]

        my_threes = self.checkForStreak(state, color, 3)
        my_twos = self.checkForStreak(state, color, 2)
        opp_threes = self.checkForStreak(state, o_color, 3)
        opp_twos = self.checkForStreak(state, o_color, 2)
        if opp_threes > 0:
            return - (10000000 * opp_threes + 100 * opp_twos)
        else:
            return my_threes * 10000000 + my_twos * 10

    def checkForStreak(self, state, color, streak):
        count = 0

        for i in range(9):
            if state[i].lower() == color.lower():
                count += self.verticalStreak(i, state, streak)
                count += self.horizontalStreak(i, state, streak)
                count += self.diagonalCheck(i, state, streak)

        return count

    def verticalStreak(self, pt, state, streak):
        consecutiveCount = 0

        for i in range(2):
            if i == 0:
                pt_check = (pt + 3) % 9
            elif i == 1:
                pt_check = (pt + 6) % 9
            if state[pt].lower() == state[pt_check].lower():
                consecutiveCount += 1

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def horizontalStreak(self, pt, state, streak):
        consecutiveCount = 0

        if pt < 3:  # pt=0,1,2
            for i in range(2):
                if i == 0:
                    pt_check = (pt + 1) % 3
                elif i == 1:
                    pt_check = (pt + 2) % 3
                if state[pt].lower() == state[pt_check].lower():
                    consecutiveCount += 1
        elif pt > 2 and pt < 6:  # pt=3,4,5
            for i in range(2):
                if i == 0:
                    pt_check = ((pt + 1) % 3) + 3
                elif i == 1:
                    pt_check = ((pt + 2) % 3) + 3
                if state[pt].lower() == state[pt_check].lower():
                    consecutiveCount += 1
        else:  # pt=6,7,8
            for i in range(2):
                if i == 0:
                    pt_check = ((pt + 1) % 3) + 6
                elif i == 1:
                    pt_check = ((pt + 2) % 3) + 6
                if state[pt].lower() == state[pt_check].lower():
                    consecutiveCount += 1

        if consecutiveCount >= streak:
            return 1
        else:
            return 0

    def diagonalCheck(self, pt, state, streak):
        total = 0
        consecutiveCount = 0

        if pt == 4:  # center
            for i in range(2):
                if i == 0:
                    pt_check = 0
                elif i == 1:
                    pt_check = 8
                if state[pt].lower() == state[pt_check].lower():
                    consecutiveCount += 1
            if consecutiveCount >= streak:
                total += 1

            consecutiveCount = 0
            for i in range(2):
                if i == 0:
                    pt_check = 2
                elif i == 1:
                    pt_check = 6
                if state[pt].lower() == state[pt_check].lower():
                    consecutiveCount += 1
            if consecutiveCount >= streak:
                total += 1

        elif pt == 0 or pt == 8:  # corner
            for i in range(2):
                if i == 0:
                    pt_check = (pt + 4) % 12
                elif i == 1:
                    pt_check = (pt + 8) % 12
                if state[pt].lower() == state[pt_check].lower():
                    consecutiveCount += 1
            if consecutiveCount >= streak:
                total += 1
        elif pt == 2 or pt == 6:  # corner
            for i in range(2):
                if i == 0:
                    pt_check = (pt + 2) % 6
                elif i == 1:
                    pt_check = (pt + 4) % 6
                if state[pt].lower() == state[pt_check].lower():
                    consecutiveCount += 1
            if consecutiveCount >= streak:
                total += 1

        # others (1, 3, 5, 7) just pass it. it's on side 

        return total
