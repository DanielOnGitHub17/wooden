from random import choice, randint, sample

MAX_WAIT_TIME = 10
username_prefixes = (
    "fighter",
    "runner",
    "quick",
    "super",
    "victorious",
    "cool",
    "amazing",
    "fast",
    "smart",
    "kind",
    "big",
    "powerful",
    "brave",
    "mighty",
    "potent",
)
DEFAULT_GRID_SIZE = 15
DEFAULT_NO_OF_PLAYERS = 10


def new_username(name):
    """Generate a new username for the user."""
    return f"{choice(username_prefixes)}{name.capitalize()}{randint(1, 400)}"


# Move to models or views
def online_players_context():
    """Get online players to be given to app views."""
    # To avoid circular import
    from game.models import Player

    return {
        "online_players": Player.objects.filter(logged_in=True).order_by("-won"),
    }


# maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def around(m, r, c):
    return sum(not x for x in (m[r - 1][c], m[r + 1][c], m[r][c - 1], m[r][c + 1]))


# Maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def make_grid(dim=15):
    """Make a bounded grid with given dimension"""
    # set result to up and down borders
    return [
        [2] * (dim + 2),
        *[[2] + [randint(0, 1) for _ in range(dim)] + [2] for _ in range(dim)],
        [2] * (dim + 2),
    ]


def get_zeros(grid):
    """Get zeros from a grid."""
    N = len(grid) - 2
    return [(i, j) for j in range(1, N) for i in range(1, N) if not grid[i][j]]


def make_game(
    dimension=DEFAULT_GRID_SIZE, no_of_players=DEFAULT_NO_OF_PLAYERS, users=[]
):
    """Make a game for the users."""
    no_of_players = len(users) or no_of_players
    player_positions = []
    while len(player_positions) < no_of_players:
        grid = make_grid(dimension)
        player_positions = get_zeros(grid)

    player_positions = sample(player_positions, no_of_players)
    return {
        "grid": grid,
        "positions": dict(zip(users, player_positions)) if users else player_positions,
    }
