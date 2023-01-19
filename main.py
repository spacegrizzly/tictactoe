import numpy as np
import pathlib as pl

import pandas as pd


def print_board(board):
    """
    todo description

    :param board:
    :return:
    """
    n = 10
    shape = board.shape

    print("\n", n * "=")
    for i in range(shape[0]):
        print(f"{board[i, 0]} | {board[i, 1]} | {board[i, 2]}")
    print(n * "=", "\n")
    print()


def replace_all(board, value: int):
    """
    Replace all
    :param board: np.array
    :param value: int, the value to use to replace all values in array
    :return: updated board
    """
    ndim = board.ndim
    shape = board.shape

    if ndim == 2:
        for i in range(shape[0]):
            for j in range(shape[1]):
                board[i, j] = value
        return board

    elif ndim == 3:
        for i in range(shape[0]):
            for j in range(shape[1]):
                for k in range(shape[2]):
                    board[i, j, k] = value

        return board

    else:
        print(f"Dimension {board.ndim} not supported. Try 2D or 3D array.")
        return -1


def create_board(specs):
    """
    Create a 2D or 3D playing board

    :param specs: specifications file
    :return: board, np.array
    """
    ndim = specs["board_ndim"]

    if ndim == 2:
        shape = (3, 3)
    elif ndim == 3:
        shape = (3, 3, 3)
    else:
        raise Exception(f"Dimension {ndim} not supported.")

    board = np.array(np.zeros(shape=shape), dtype=int)
    replace_all(board, -1)
    return board


def decide_on_token(game_status: dict):
    tokens = [1, 2]

    if game_status["no_of_players"] == 2:
        game_status["token_p1"] = tokens[0]
        game_status["token_p2"] = tokens[1]
    else:
        raise Exception("Only 2 players accepted at this time.")

    return game_status


def get_move(board, game_status: dict):
    """
    todo: fill in

    :param board:
    :param game_status:
    :return:
    """
    active_player = game_status["active_player"]

    print(f"Player {active_player}, your turn!")

    print(f"Make a move (choose x pos (1-3):")
    choice_x = int(input(int))

    print(f"Make a move (choose y pos (1-3):")
    choice_y = int(input(int))

    if choice_x >= 1 & choice_x <= 3 & choice_y >= 1 & choice_y <= 3:
        if board[choice_x - 1, choice_y - 1] == -1:
            board[choice_x - 1, choice_y - 1] = game_status[f"token_p{active_player}"]
        else:
            raise Exception("Position already taken")
            # todo: this needs work
    else:
        raise Exception("Choice out of range!")

    return 0


def check_win(board, game_status):
    check_diagonal(board, game_status)
    check_vertical(board, game_status)
    check_horizontal(board, game_status)

    if not game_status["game_running"]:
        ap = game_status["active_player"]
        game_status["winner"] = ap

        n = 35
        print(n * "=")
        print(f"Congratulations, Player {ap} -- you won!")
        print(n * "=")

    return 0


def check_diagonal(board, game_status):
    if board[0, 0] == board[1, 1] == board[2, 2] and board[0, 0] != -1:
        game_status["game_running"] = False
    elif board[0, 2] == board[1, 1] == board[2, 0] and board[0, 2] != -1:
        game_status["game_running"] = False

    return 0


def check_vertical(board, game_status):
    for j in range(3):
        if board[0, j] == board[1, j] == board[2, j] and board[0, j] != -1:
            game_status["game_running"] = False
    return 0


def check_horizontal(board, game_status):
    for i in range(3):
        if board[i, 0] == board[i, 1] == board[i, 2] and board[i, 0] != -1:
            game_status["game_running"] = False
    return 0


def check_draw(board, game_status):
    if -1 not in board:
        game_status["draw"] = True
        game_status["game_running"] = False

        print("Game is a draw. Shake hands.")


def switch_player(game_status):
    if game_status["active_player"] == 1:
        game_status["active_player"] = 2
    else:
        game_status["active_player"] = 1


def plot_board(board, export: bool = False):
    import plotly.graph_objects as go
    import itertools
    template = "simple_white"
    # template = "plotly_dark"
    fig = go.Figure()
    fig.update_layout(title="",
                      # xaxis_title="x (au)",
                      # yaxis_title="y (au)",
                      template=template,
                      autosize=False,
                      width=1000,
                      height=1000,
                      margin=dict(l=100, r=100, b=100, t=100, pad=4)
                      )

    xpos_lst = [0, 1, 2]
    ypos_lst = [0, 1, 2]
    df_board = []
    for r in itertools.product(xpos_lst, ypos_lst):
        df_board.append([r[0], r[1], pd.DataFrame(board)[r[0]][r[1]]])

    df_board = pd.DataFrame(df_board, columns=["x", "y", "value"])

    fig.add_trace(go.Scattergl(x=df_board[df_board.value == -1].x, y=df_board[df_board.value == -1].y,
                               mode='markers',
                               marker=dict(color="grey", size=200)
                               ))

    fig.add_trace(go.Scattergl(x=df_board[df_board.value == 1].x, y=df_board[df_board.value == 1].y,
                               mode='markers',
                               marker=dict(color="blue", size=200)
                               ))

    fig.add_trace(go.Scattergl(x=df_board[df_board.value == 2].x, y=df_board[df_board.value == 2].y,
                               mode='markers',
                               marker=dict(color="yellow", size=200)
                               ))

    if export:
        path_out = pl.Path(config["path_out"], "plot.html")
        path_out.parent.mkdir(exist_ok=True)
        fig.write_html(str(path_out))

    fig.show()
    return 0


def main():
    # this is intended for the player to decide before commencing
    specs = {"board_ndim": 2,  # valid input 2 or 3
             "no_of_players": 2,  #
             "computer": False,
             }

    # this is intended as internal game status
    game_status = {"game_running": True,
                   "active_player": -1,
                   "winner": -1,
                   "draw": False,
                   "board_ndim": specs["board_ndim"],
                   "no_of_players": specs["no_of_players"],
                   "computer": specs["computer"],
                   }

    board = create_board(specs)
    print_board(board)
    plot_board(board)
    decide_on_token(game_status)
    game_status["active_player"] = np.random.randint(1, 3)

    while game_status["game_running"]:
        get_move(board, game_status)
        print_board(board)
        plot_board(board)
        check_win(board, game_status)
        check_draw(board, game_status)
        switch_player(game_status)


if __name__ == '__main__':
    main()
