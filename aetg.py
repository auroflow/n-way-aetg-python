import itertools
from copy import copy
import random


class AETG:

    def __init__(self, params: list, dimension=2, num_random_cases=50):
        # number of possible values of each parameter
        self.params = copy(params)
        # how-many-way combination is required
        self.dimension = dimension
        # number of random test cases generated in one iteration
        self.M = num_random_cases
        # self.M-way combination of parameters
        self.param_tuples = []
        for combination in itertools.combinations(range(len(params)), self.dimension):
            self.param_tuples.append(combination)
        # combinations to cover. A combination is represented by ((p1, v1), (p2, v2), (p3, v3), ...)
        self.uncovered = set()
        # occurrences of (param, value) pairs in uncovered combinations
        self.occurrences = dict()
        for param_tuple in self.param_tuples:
            # param_tuple is an instance of (p1, p2, p3, ...)
            # more_combs is a set of (v1, v2, v3, ...)
            more_combs = itertools.product(*[range(self.params[i]) for i in param_tuple])
            for comb in more_combs:
                pv_pairs = tuple(zip(param_tuple, comb))
                print(pv_pairs)
                for pv_pair in pv_pairs:
                    self.occurrences[pv_pair] = self.occurrences.get(pv_pair, 0) + 1
                self.uncovered.add(pv_pairs)
        # max number of possible test cases
        self.max_num_cases = int(1)
        for v_count in self.params:
            self.max_num_cases *= v_count
        # test cases generated with AETG algorithm
        self.cases = None

    def generate(self):
        if self.cases is not None:
            return self.cases
        cases = []

        while len(self.uncovered):
            # First generate self.M different candidate test cases.
            # Choose a parameter f and a value l for f such that that parameter value
            # appears in the greatest number of uncovered pairs.
            f, l = max(self.occurrences, key=self.occurrences.get)
            candidates = []
            while len(candidates) < self.M:
                # Let f1 = f. Then choose a random order for the remaining parameters.
                indices = list(range(len(self.params)))
                indices[0], indices[f] = indices[f], indices[0]
                indices[1:] = random.sample(indices[1:], len(indices) - 1)

                case = []
                for i, param in enumerate(indices):
                    for value in range(self.params[param]):

            # param_tuple = random.choice(self.param_tuples)
            # test_case = []
            # for i in param_tuple:
            #     test_case.append((i, random.randrange(0, self.params[i])))
            # test_case = tuple(test_case)
            # if test_case not in candidates and test_case not in cases:
            #     candidates.append(test_case)
            break
        # cache result
        self.cases = cases
        return cases


if __name__ == '__main__':
    aetg = AETG([2, 3, 5], 2)
    print(len(aetg.uncovered))
    print(aetg.occurrences)
    aetg.generate()
