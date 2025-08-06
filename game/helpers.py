from random import choice, randint, sample

MAX_WAIT_TIME = 10
username_prefixes = ("fighter", "runner", "quick", "super", "victorious",
                     "cool", "amazing", "fast", "smart", "kind", "big",
                       "powerful", "brave", "mighty", "potent")

def new_username(name):
    """Generate a new username for the user."""
    return f"{choice(username_prefixes)}{name.capitalize()}{randint(10, 400)}"

def online_players_context():
    """Get online players to be given to app views."""
     # To avoid circular import
    from game.models import Player  # pylint: disable=import-outside-toplevel
    return {
        "online_players": Player.objects.filter(logged_in=True).order_by("-won"),  # pylint: disable=no-member
    }


# maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def around(m, r, c):
    return sum(not x for x in (m[r-1][c], m[r+1][c], m[r][c-1], m[r][c+1]))


# Maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def make_grid(dim=15):
    """Make a grid for the game."""
    # set result to up and down borders
    return [
        [2] * (dim+2),
        *[
            *map(lambda x: [2]+list(map(lambda i: randint(0, 1), range(dim)))+[2], range(dim))
        ],
        [2] * (dim+2),
    ]

def get_zeros(grid):
    """Get zeros from the grid."""
    N = len(grid) + 1
    return [(i, j) for j in range(1, N) for i in range(1, N) if not grid[i][j]]

def make_game(n=7, users=None):
    """Make a game for the users."""
    if users is None:
        users = []
    n = len(users) or n
    zeros = []
    while len(zeros) < n:
        grid = make_grid()
        zeros = get_zeros(grid)
    zeros = sample(zeros, n)
    return {
        "grid": grid,
        "positions": {user: pos for user, pos in zip(users, zeros)}\
              if users else zeros,
    }
