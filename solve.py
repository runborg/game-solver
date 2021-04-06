#!/usr/bin/env python3

from enum import Enum
from collections import defaultdict
from pprint import pprint
import time


class DIR(Enum):
    UP = 'U',
    DOWN = 'D',
    LEFT = 'L',
    RIGHT = 'R',


class NoWrapList(list):
    def __getitem__(self, item):
        if isinstance(item, int):
            if item < 0:
                raise ValueError('Ehrm, under zero? :S')
        return super(NoWrapList, self).__getitem__(item)


init_board = NoWrapList([
              NoWrapList([ ' ', ' ', ' ', 'I', 'I', 'I', ' ', ' ', ' ']),
              NoWrapList([ ' ', ' ', ' ', 'I', 'I', 'I', ' ', ' ', ' ']),
              NoWrapList([ ' ', ' ', ' ', 'I', 'I', 'I', ' ', ' ', ' ']),
              NoWrapList([ 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I']),
              NoWrapList([ 'I', 'I', 'I', 'I', 'O', 'I', 'I', 'I', 'I']),
              NoWrapList([ 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I', 'I']),
              NoWrapList([ ' ', ' ', ' ', 'I', 'I', 'I', ' ', ' ', ' ']),
              NoWrapList([ ' ', ' ', ' ', 'I', 'I', 'I', ' ', ' ', ' ']),
              NoWrapList([ ' ', ' ', ' ', 'I', 'I', 'I', ' ', ' ', ' ']),
             ])


def count(board):
    return sum([len([y for y in x if y == 'I']) for x in board])


def check_isolated(board, first_only=False):
    isolated = []
    for y in range(9):
        for x in range(9):
            if board[y][x] != 'I':
                continue
            # Check left side
            if y > 1 and board[y-2][x] == 'I':
                continue
            if y > 0 and board[y-1][x] == 'I':
                continue

            # Check right side
            if y < 7 and board[y+2][x] == 'I':
                continue
            if y < 8 and board[y+1][x] == 'I':
                continue

            # Check Up side
            if x > 1 and board[y][x-2] == 'I':
                continue
            if x > 0 and board[y][x-1] == 'I':
                continue

            # Check down side
            if x < 7 and board[y][x+2] == 'I':
                continue
            if x < 8 and board[y][x+1] == 'I':
                continue

            # Check upper/lower left
            if y > 0 and x > 0 and board[y-1][x-1] == 'I':
                continue
            if y < 8 and x > 0 and board[y+1][x-1] == 'I':
                continue
            # Check upper/lower right
            if y > 0 and x < 8 and board[y-1][x+1] == 'I':
                continue
            if y < 8 and x < 8 and board[y+1][x+1] == 'I':
                continue
            if first_only:
                return [(y, x)]
            isolated.append((y, x))
    return isolated


def yield_moveable(board):
    for y in range(9):
        for x in range(9):
            # Check for moveable object on position
            if board[y][x] != 'I':
                continue
            # Test Left
            if x > 1 and board[y][x-1] == 'I' and board[y][x-2] == 'O':
                yield y, x, DIR.LEFT
            # Test Right
            if x < 7 and board[y][x+1] == 'I' and board[y][x+2] == 'O':
                yield y, x, DIR.RIGHT
            # Test Up
            if y > 1 and board[y-1][x] == 'I' and board[y-2][x] == 'O':
                yield y, x, DIR.UP
            # Test Down
            if y < 7 and board[y+1][x] == 'I' and board[y+2][x] == 'O':
                yield y, x, DIR.DOWN


def moveable(board, y, x, dir):
    # Test if this position is movable
    if board[y][x] != 'I':
        return False

    # Test neighbor position if its empty
    if dir == DIR.LEFT:
        if x > 1 and board[y][x-2] == 'O':
            return True
    elif dir == DIR.RIGHT:
        if x < 7 and board[y][x+2] == 'O':
            return True
    elif dir == DIR.UP:
        if y > 1 and board[y-2][x] == 'O':
            return True
    elif dir == DIR.DOWN:
        if y < 7 and board[y+2][x] == 'O':
            return True
    return False


def move(board, y, x, dir):
    try:
        if dir == DIR.LEFT:
            if not board[y][x-1] == 'I':
                raise Exception('Unable to move y%sx%s in direction %s, Nothing to jump over' % (y, x, dir))
            if not board[y][x-2] == 'O':
                raise Exception('Unable to move y%sx%s in direction %s, Target is occupied' % (y, x, dir))

            board[y][x-2] = 'I'
            board[y][x-1] = 'O'
            board[y][x-0] = 'O'

        elif dir == DIR.RIGHT:
            if not board[y][x+1] == 'I':
                raise Exception('Unable to move y%sx%s in direction %s, Nothing to jump over' % (y, x, dir))
            if not board[y][x+2] == 'O':
                raise Exception('Unable to move y%sx%s in direction %s, Target is occupied' % (y, x, dir))
            board[y][x+2] = 'I'
            board[y][x+1] = 'O'
            board[y][x+0] = 'O'

        elif dir == DIR.UP:
            if not board[y-1][x] == 'I':
                raise Exception('Unable to move y%sx%s in direction %s, Nothing to jump over' % (y, x, dir))
            if not board[y-2][x] == 'O':
                raise Exception('Unable to move y%sx%s in direction %s, Target is occupied' % (y, x, dir))
            board[y-2][x] = 'I'
            board[y-1][x] = 'O'
            board[y-0][x] = 'O'

        elif dir == DIR.DOWN:
            if not board[y+1][x] == 'I':
                raise Exception('Unable to move y%sx%s in direction %s, Nothing to jump over' % (y, x, dir))
            if not board[y+2][x] == 'O':
                raise Exception('Unable to move y%sx%s in direction %s, Target is occupied' % (y, x, dir))
            board[y+2][x] = 'I'
            board[y+1][x] = 'O'
            board[y+0][x] = 'O'
        else:
            raise Exception('Unable to move y%sx%s in direction %s, Unknown direction' % (y, x, repr(dir)))
    except IndexError:
        raise Exception('Unable to move y%sx%s in direction %s, To near the edge' % (y, x, dir))


def undo(board, y, x, dir):
    try:
        if dir == DIR.LEFT:
            if not (board[y][x-2] == 'I' and board[y][x-1] == 'O' and board[y][x-0] == 'O'):
                raise Exception('Unable to undo y%sx%s in direction %s, not a valid move' % (y, x, dir))
            board[y][x-2] = 'O'
            board[y][x-1] = 'I'
            board[y][x-0] = 'I'

        elif dir == DIR.RIGHT:
            if not (board[y][x+2] == 'I' and board[y][x+1] == 'O' and board[y][x+0] == 'O'):
                raise Exception('Unable to undo y%sx%s in direction %s, not a valid move' % (y, x, dir))
            board[y][x+2] = 'O'
            board[y][x+1] = 'I'
            board[y][x+0] = 'I'

        elif dir == DIR.UP:
            if not (board[y-2][x] == 'I' and board[y-1][x] == 'O' and board[y-0][x] == 'O'):
                raise Exception('Unable to undo y%sx%s in direction %s, not a valid move' % (y, x, dir))
            board[y-2][x] = 'O'
            board[y-1][x] = 'I'
            board[y-0][x] = 'I'

        elif dir == DIR.DOWN:
            if not (board[y+2][x] == 'I' and board[y+1][x] == 'O' and board[y+0][x] == 'O'):
                raise Exception('Unable to undo y%sx%s in direction %s, not a valid move' % (y, x, dir))
            board[y+2][x] = 'O'
            board[y+1][x] = 'I'
            board[y+0][x] = 'I'
        else:
            raise Exception('Unable to undo y%sx%s in direction %s, Unknown direction' % (y, x, repr(dir)))
    except IndexError:
        raise Exception('Unable to undo y%sx%s in direction %s, To near the edge' % (y, x, dir))



def print_board(board):
    print("  0 1 2 3 4 5 6 7 8 X")
    for i, x in enumerate(board):
        print(i, " ".join(x))
    print("Y")


nr = 0
result = []
tries = 0
le = defaultdict(int)
last_time = time.time()


def solve(board, stack=0):
    global tries, result, nr, le, last_time
    tries += 1

    if stack <= 25:
        le[stack] += 1
    if stack == 25:
        now_time = time.time()
        pprint(le)
        print_board(board)
        print('Count %010d  runtime %5.2f  stackcount %3d  on-board %3d' % (tries, now_time-last_time,  stack, count(board)))
        last_time = now_time

    # If isolated elements are found in this board, just send back.. its not solvable
    if check_isolated(board, first_only=True):
        return False

    for x in yield_moveable(board):
        move(board, *x)
        if count(board) == 1:
            result.append(*x)
            return True
        if solve(board, stack=stack+1):
            print('Test Passed! wee!')
            result.append(*x)
            return True
        undo(board, *x)
    return False


def main():
    print('Initial Board Layout')
    print_board(init_board)
    # for x in yield_moveable(init_board):
    #     print(f'Move y{x[0]}x{x[1]} {x[2]!r}')
    #     move(init_board, *x)
    #     print_board(init_board)
    #     undo(init_board, *x)
    #     print_board(init_board)
    start = time.time()
    solve(init_board)
    end = time.time()
    delta = end - start
    print("type delta", type(delta))
    print(end - start)

    # for i, s in enumerate(result):
    #     print('%04d   %s' % (i , s))
    # print('Current Board')
    # print_board(init_board)
    print("Number", nr)

    # for i in yield_moveable(init_board):
    #     print(i)
    # return


if __name__ == "__main__":
    main()
