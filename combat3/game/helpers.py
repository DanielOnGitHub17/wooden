from random import randint


# maze algorithm. 0, 1, 2. 0=space. 1=wood(breakable), 2=iron(protective)
def make_game(dim):
    result = []
    for i in range(dim):
        result.append([])
        for j in range(dim):
            result[-1].append(randint(0, 1))
    return result