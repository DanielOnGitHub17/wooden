from random import randint


# maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def around(m, r, c):
    zero_length = 0
    for x in (m[r-1][c], m[r+1][c], m[r][c-1], m[r][c+1]):
        if not x:
            zero_length += 1
    return zero_length

zero_based_choosing = [(0, 0), (0, 0), (0, 2), (0, 2), (1, 2)]

def make_game(dim):
    # set result to up and down borders
    result = [
        [2] * (dim+2),
        *[[2]+[randint(0, 2) for i in range(dim)]+[2] for i in range(dim)],
        [2] * (dim+2),
    ]
    with open("maze.txt", 'w') as maze:
        maze.write('\n'.join(str(line) for line in result))
    for r in range(1, dim+1):
        for c in range(1, dim+1):
            #  self      up       down      left     right
            # [r][c]  [r-1][c]  [r+1][c]  [r][c-1]  [r][c+1]
            # {4: (1, 2), 3: (0, 2), 2: (0, 1), 1, 0: (0)}
            result[r][c] = randint(*zero_based_choosing[around(result, r, c)])

    return result