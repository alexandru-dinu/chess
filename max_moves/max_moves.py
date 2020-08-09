import asyncio
from tqdm import tqdm
import numpy as np
import pickle
import multiprocessing as mp

import gc

import sys

import chess
import chess.engine

"""
Related to
https://chess.stackexchange.com/questions/31745/forced-mate-2-queens-vs-king

TODO: cache positions (FEN) to results
"""


def generate_all():
    xs = []

    board = chess.Board()
    board.clear_board()

    ps = set(list(chess.SQUARES))

    for p1 in tqdm(ps):
        for p2 in (ps - {p1}):
            for p3 in (ps - {p1, p2}):
                for p4 in (ps - {p1, p2, p3}):
                    board = chess.Board()
                    board.clear_board()

                    board.set_piece_at(p1, chess.Piece(chess.KING, chess.WHITE))
                    board.set_piece_at(p2, chess.Piece(chess.QUEEN, chess.WHITE))
                    board.set_piece_at(p3, chess.Piece(chess.QUEEN, chess.WHITE))
                    board.set_piece_at(p4, chess.Piece(chess.KING, chess.BLACK))
                    board.turn = chess.BLACK

                    if board.is_check():
                        continue

                    else:
                        board.turn = chess.WHITE
                        xs += [board.fen()]

    return xs



def generate_random():
    board = chess.Board()
    board.clear_board()

    board.turn = chess.BLACK

    pos = np.random.choice(chess.SQUARES, replace=False, size=(3,))

    for i, p in enumerate([chess.KING, chess.QUEEN, chess.QUEEN]):
        board.set_piece_at(pos[i], chess.Piece(p, chess.WHITE))

    while True:
        p = np.random.choice(chess.SQUARES)

        if p in pos:
            continue

        board.set_piece_at(p, chess.Piece(chess.KING, chess.BLACK))
        if board.is_check():
            board.remove_piece_at(p)
            continue

        break

    board.turn = chess.WHITE

    return board


async def play(board):
    l = 0

    transport, engine = await chess.engine.popen_uci("/usr/bin/stockfish")

    while not board.is_game_over():
        result = await engine.play(board, chess.engine.Limit(time=1.0))
        board.push(result.move)
        l += 1

    await engine.quit()

    return l if board.is_checkmate() else None


if __name__ == "__main__":
    d = {}
    fens = pickle.load(open('boards.pkl', 'rb'))

    asyncio.set_event_loop_policy(chess.engine.EventLoopPolicy())
    for fen in tqdm(fens):
        d[fen] = asyncio.run(play(chess.Board(fen=fen)))

    pickle.dump(d, open('boards_res.pkl', 'wb'))
