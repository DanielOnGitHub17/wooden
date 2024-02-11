from random import randint


def make_game(dim):
    result = []
    for i in dim:
        result.append[[]]
        for j in dim:
            result[-1].append(randint(0, 1))
    return result