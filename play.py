# coding: UTF-8
import Minimax


class Game(object):
    '''
    board list:        player key-in:
            012                    789
            345                    456
            678                    123
    '''
    player = [None, None]
    color = ['O', 'X']
    round = None
    turn = None
    finished = None
    winner = None
    board = None

    def __init__(self):
        print('\n' * 100)

        while self.player[0] == None:
            playerType = str(input("Is player1 Human or Computer? "))
            if playerType.lower() == 'h' or playerType.lower() == 'human':
                name = str(input("What's player1's name? "))
                self.player[0] = Player(name, self.color[0])
            elif playerType.lower() == 'c' or playerType.lower() == 'computer':
                self.player[0] = AIPlayer('Mr. Minimax', self.color[0], difficulty = 5)
            else:
                print('Please enter < Human / H > or < Computer / C >')
        while self.player[1] == None:
            playerType = str(input("Is player2 Human or Computer? "))
            if playerType.lower() == 'h' or playerType.lower() == 'human':
                name = str(input("What's player2's name? "))
                self.player[1] = Player(name, self.color[1])
            elif playerType.lower() == 'c' or playerType.lower() == 'computer':
                self.player[1] = AIPlayer('Ms. Minimax', self.color[1], difficulty = 5)
            else:
                print('Please enter < Human / H > or < Computer / C >')
        self.round = 1
        self.turn = self.player[0]
        self.finished = False
        self.winner = None
        self.board = ['-'] * 9
        return

    def nextMove(self):
        player = self.turn

        if self.round > 9:
            self.finished = True
            return
        move = player.move(self.board)

        if self.board[move] == '-':
            self.board[move] = player.color
            self.switchTurn()
            self.isWin()
            self.printState()
            return
        # 指定位置已有棋子
        print("I think that's not a good choice... Make another choice.")
        return

    def switchTurn(self):
        if self.turn == self.player[0]:
            self.turn = self.player[1]
        else:
            self.turn = self.player[0]
        self.round += 1
        return

    def printState(self):
        #         print('\n'*100)
        print('Round: {}'.format(self.round))
        print('\t 789  ', end = "")
        for i in range(9):
            if (i + 1) % 3 == 0:
                if i == 2:
                    print('{}'.format(self.board[i]), end = "\n\t 456  ")
                elif i == 5:
                    print('{}'.format(self.board[i]), end = "\n\t 123  ")
                else:
                    print('{}'.format(self.board[i]), end = "\n")
            else:
                print('{}'.format(self.board[i]), end = "")
        if self.finished:
            print("Game Over")
            if self.winner != None:
                print(str(self.winner.name) + " is the winner")
            else:
                print('Draw')
        return

    def isWin(self):
        for i in range(0, 7, 3):
            if self.board[i] == self.board[i + 1] == self.board[i + 2] != '-':
                if self.round % 2 == 0:
                    self.winner = self.player[0]
                else:
                    self.winner = self.player[1]
                self.finished = True
                return
        for i in range(3):
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != '-':
                if self.round % 2 == 0:
                    self.winner = self.player[0]
                else:
                    self.winner = self.player[1]
                self.finished = True
                return
        if (self.board[0] == self.board[4] == self.board[8] != '-') or (
                self.board[2] == self.board[4] == self.board[6] != '-'):
            if self.round % 2 == 0:
                self.winner = self.player[0]
            else:
                self.winner = self.player[1]
            self.finished = True
            return

    def newGame(self):
        self.round = 1
        self.turn = self.player[0]
        self.finished = False
        self.winner = None
        self.board = ['-'] * 9
        return


class Player(object):
    type = None
    name = None
    color = None

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.type = 'Human'
        return

    def move(self, state):
        '''
        user key-in > board list 
        789 > 012
        456 > 345
        123 > 678
        '''
        mapKeyIn = {
            7: 0, 8: 1, 9: 2,
            4: 3, 5: 4, 6: 5,
            1: 6, 2: 7, 3: 8
        }
        print("{0}'s turn {0} is {1}".format(self.name, self.color))
        choice = None
        while choice == None:
            try:
                choice = int(input('Enter 1-9: '))
                if choice > 9 or choice < 1:
                    choice = None
                    print('Value error! You need to enter a number between 1 and 9')
            except Exception:
                choice = None
                print('Value error! You need to enter a integer number')
        return (mapKeyIn[choice])


class AIPlayer(Player):
    type = None
    name = None
    color = None
    difficulty = None

    def __init__(self, name, color, difficulty = 50):
        self.name = name
        self.color = color
        self.type = 'AI'
        self.difficulty = difficulty

    def move(self, state):
        m = Minimax.Minimax(state)
        best_move, value = m.bestMove(self.difficulty, state, self.color)
        return best_move


def main():
    g = Game()
    g.printState()
    player1 = g.player[0]
    player2 = g.player[1]

    win_counts = [0, 0, 0]  # [p1 wins, p2 wins, ties]
    exit = False
    while not exit:
        while not g.finished:
            g.nextMove()

        if g.winner == None:
            win_counts[2] += 1
        elif g.winner == player1:
            win_counts[0] += 1
        elif g.winner == player2:
            win_counts[1] += 1

        printStats(player1, player2, win_counts)
        while True:
            again = str(input('Play again? '))
            if again.lower() == 'no' or again.lower() == 'n':
                print('Bye!')
                exit = True
                break
            elif again.lower() == 'yes' or again.lower() == 'y':
                g.newGame()
                g.printState()
                break
            else:
                print('Please enter Yes (y) or No (n)')


def printStats(player1, player2, win_counts):
    print('{}: {} wins, {}: {} wins, {} ties'.format(player1.name,
                                                     win_counts[0], player2.name, win_counts[1], win_counts[2]))


main()
