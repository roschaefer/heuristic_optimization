from multiprocessing import Pool
import ant_colony


def run(args):
    return ant_colony.Solver(*args).find_optimum()


if __name__ == '__main__':

    with Pool(processes=4) as pool:
        print(pool.map(run, [
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

    # ant_colony.Solver('gr17', optimum=2085, RHO=0.99, ALPHA=1, BETA=0).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.9, ALPHA=1, BETA=2).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=1, BETA=0).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.7, ALPHA=1, BETA=0).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.5, ALPHA=1, BETA=0).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.1, ALPHA=1, BETA=0).find_optimum()


    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=1, BETA=1).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=1, BETA=2).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=1, BETA=4).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=1, BETA=8).find_optimum()


    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=0, BETA=0).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=1, BETA=0).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=2, BETA=0).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=4, BETA=0).find_optimum()
    # ant_colony.Solver('gr17', optimum=2085, RHO=0.8, ALPHA=8, BETA=0).find_optimum()
