import pandas as pd
import numpy as np
from utils import read_input


def main(boards, numbers, n_boards, win_first=True):
    boards_df, empty_boards_df = create_board_dfs(boards)
    n_boards_won = 0
    boards_already_won = []
    for n in numbers:
        for b in range(n_boards):
            if debug:
                print(n, b)
            find_mark_number_in_dfs(boards_df[b], empty_boards_df[b], n)
            if b in boards_already_won:
                continue
            row_or_col, idx_or_key = check_row_col_completeness(empty_boards_df[b])
            if row_or_col:
                sum_unmarked = get_sum_unmarked(boards_df[b], empty_boards_df[b])
                if win_first:
                    return sum_unmarked, n
                else:
                    boards_already_won.append(b)
                    n_boards_won += 1
                    if n_boards_won == n_boards:
                        return sum_unmarked, n


def create_board_dfs(boards):
    boards_df, empty_boards_df = [], []
    for b in boards:
        board = np.array([int(n) for n in b[1].split()])
        board = np.expand_dims(board, axis=0)
        for l in b[2:]:
            board = np.append(board, [[int(n) for n in l.split()]], axis=0)
        boards_df.append(pd.DataFrame(board))
        empty_boards_df.append(pd.DataFrame(np.zeros(boards_df[0].shape, dtype=int)))
    return boards_df, empty_boards_df


def find_mark_number_in_dfs(b_df, e_df, n):
    for c in b_df.columns:
        if (b_df[c] == n).sum() > 0:
            idx = b_df[b_df[c] == n].index
            e_df.loc[idx, c] = 1
            return


def check_row_col_completeness(df):
    row_or_col = False
    idx_or_key = False
    for c in df.columns:
        if df[c].sum() == df.shape[0]:
            return 'c', c
    for i in range(df.shape[0]):
        if df.loc[i].sum() == len(df.columns):
            return 'r', i
    return row_or_col, idx_or_key


def get_sum_unmarked(b_df, e_df):
    sum = 0
    if debug:
        print(b_df)
        print(e_df)
    for c in e_df.columns:
        idx_not_marked = e_df.index[e_df[c] != 1].tolist()
        sum += b_df.loc[idx_not_marked][c].sum()
    return sum


debug = False
files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:

    input = read_input(f)
    numbers = [int(n) for n in input[0].split(',')]
    n_boards = len([l for l in input[1:] if l == ""])
    boards = np.array_split(input[1:], n_boards)

    s, n = main(boards, numbers, n_boards)
    print(f"{f} - Part 1: {s} * {n} = {s*n}")
    s, n = main(boards, numbers, n_boards, win_first=False)
    print(f"{f} - Part 2: {s} * {n} = {s * n}")
