import contextlib
from multiprocessing import Pool
import ant_colony


def run(args):
    return ant_colony.Solver(*args).find_optimum()


if __name__ == '__main__':

    with contextlib.closing(Pool(processes=4)) as pool:
        print(pool.map(run, 10 * [
            #        optimum, RHO,  ALPHA, BETA
            ('gr17', 2085,    0.99,   1,   0),
            ('gr17', 2085,    0.9,    1,   0),
            ('gr17', 2085,    0.8,    1,   0),
            ('gr17', 2085,    0.7,    1,   0),
            ('gr17', 2085,    0.5,    1,   0),
            ('gr17', 2085,    0.1,    1,   0),
            ('gr17', 2085,    0.8,    0,   1),
            ('gr17', 2085,    0.8,    1,   1),
            ('gr17', 2085,    0.8,    1,   2),
            ('gr17', 2085,    0.8,    1,   4),
            ('gr17', 2085,    0.8,    1,   8),
            ('gr17', 2085,    0.8,    0,   0),
            ('gr17', 2085,    0.8,    1,   0),
            ('gr17', 2085,    0.8,    2,   0),
            ('gr17', 2085,    0.8,    4,   0),
            ('gr17', 2085,    0.8,    8,   0),
        ]))
