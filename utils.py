import numpy as np
import matplotlib.pyplot as plt

import chess.pgn


def stem_hist(xs, show=False):
    x, f = np.unique(xs, return_counts=True)
    f = f / f.sum()
    plt.stem(x, f, use_line_collection=True)
    plt.xticks(x)
    if show:
        plt.show()
        
        
def get_games(pgn_file, n):
    with open(pgn_file) as pgn:
        return [chess.pgn.read_game(pgn) for _ in range(n)]