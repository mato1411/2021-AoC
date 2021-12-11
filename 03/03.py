import pandas as pd
import numpy as np
from utils import read_input


def process_ox_co2_ratings(df, more_1_bits_eq, less_1_bits_eq):
    idx = df.index
    for c in df.columns:
        n_records_left = df.loc[idx][c].notnull().sum()
        if n_records_left > 1:
            if df.loc[idx][c].sum() >= n_records_left/2: # More 1 bits
                idx = df.loc[df.index.isin(idx) & (df[c] == more_1_bits_eq)].index
            else: # More 0 bits
                idx = df.loc[df.index.isin(idx) & (df[c] == less_1_bits_eq)].index
        else:
            break
    return idx


files = ['example.txt', 'input.txt', 'input2.txt']

for f in files:
    binaries = read_input(f)
    x = np.array(list(map(int, binaries[0])))
    x = np.expand_dims(x, axis=0)
    for n in binaries[1:]:
        x = np.append(x, [list(map(int, list(n)))], axis=0)
    df = pd.DataFrame(x)

    gamma_bool = (df.sum() > df.shape[0]/2)
    gamma_bin = "".join([str(i) for i in gamma_bool.apply(lambda x: int(x)).values])
    gamma_dec = int(gamma_bin, 2)
    eps_bool = ~gamma_bool
    eps_bin = "".join([str(i) for i in eps_bool.apply(lambda x: int(x)).values])
    eps_dec = int(eps_bin, 2)

    df_ox_idx = process_ox_co2_ratings(df, 1, 0)
    ox_bin = "".join([str(i) for i in df.loc[df_ox_idx].values[0]])
    ox_dec = int(ox_bin, 2)

    df_co_idx = process_ox_co2_ratings(df, 0, 1)
    co_bin = "".join([str(i) for i in df.loc[df_co_idx].values[0]])
    co_dec = int(co_bin, 2)

    print(f"{f} - Part 1: {gamma_dec} * {eps_dec} = {gamma_dec*eps_dec}")
    print(f"{f} - Part 2: {ox_dec} * {co_dec} = {ox_dec*co_dec}")
