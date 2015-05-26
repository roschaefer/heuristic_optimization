import contextlib
from multiprocessing import Pool
import ant_colony


def run(args):
    print (args)
    return ant_colony.Solver(*args).find_optimum()


if __name__ == '__main__':

    with contextlib.closing(Pool(processes=4)) as pool:
        pool.map(run, 10 * [
            #        optimum, RHO,  ALPHA, BETA
            ('gr17', 2085,    0.8,    3,   0),
            ('gr17', 2085,    0.8,    2,   2),
            ('gr17', 2085,    0.8,    1,   4),
            ('gr17', 2085,    0.8,    0.1,   8),

            ('fri26', 937,    0.8,    3,   0),
            ('fri26', 937,    0.8,    2,   2),
            ('fri26', 937,    0.8,    1,   4),
            ('fri26', 937,    0.8,    0.1,   8),

            ('gr17', 2085,    0.5,    3,   0),
            ('gr17', 2085,    0.5,    2,   2),
            ('gr17', 2085,    0.5,    1,   4),
            ('gr17', 2085,    0.5,    0.1,   8),

            ('fri26', 937,    0.5,    3,   0),
            ('fri26', 937,    0.5,    2,   2),
            ('fri26', 937,    0.5,    1,   4),
            ('fri26', 937,    0.5,    0.1,   8),

            ('gr17', 2085,    0.1,    3,   0),
            ('gr17', 2085,    0.1,    2,   2),
            ('gr17', 2085,    0.1,    1,   4),
            ('gr17', 2085,    0.1,    0.1,   8),

            ('fri26', 937,    0.1,    3,   0),
            ('fri26', 937,    0.1,    2,   2),
            ('fri26', 937,    0.1,    1,   4),
            ('fri26', 937,    0.1,    0.1,   8),

        ])
        # parameters from paper
        pool.map(run, 10 * [
            ('gr17', 2085,    0.8,    1,   2),
            ('fri26', 937,    0.8,    1,   2)
        ])
