from random import randint


# maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def around(m, r, c):
    zero_length = 0
    for x in (m[r-1][c], m[r+1][c], m[r][c-1], m[r][c+1]):
        if not x:
            zero_length += 1
    return zero_length


