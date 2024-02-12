from random import randint


# maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def around(m, r, c):
    (m[r-1][c], m[r+1][c], m[r][c-1], m[r][c+1])
    return 

def make_game(dim):
    # set result to up and down borders
    result = [
        [2] * (dim+2),
        *[[2]+[randint(0, 2) for i in range(dim)]+[2] for i in range(dim)],
        [2] * (dim+2),
    ]
    for r in range(1, dim+1):
        for c in range(1, dim+1):
            #  self      up       down      left     right
            # [r][c]  [r-1][c]  [r+1][c]  [r][c-1]  [r][c+1]
            neighbours = around(result, r, c)

    return result