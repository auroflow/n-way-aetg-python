from tqdm import tqdm
import random
import itertools


# `dim` = N
# `v_count` is a list that specifies the number of possible values for each param.
# `pair` stands for an N-way (param, value) combination, e.g. ((p1, v1), (p2, v2), (p3, v3), ...)
# `p_pair` stands for an N-way param combination, e.g. (p1, p2, p3, ...)
# `pv_pair` stands for a (param, value) pair (that is really a "pair"), e.g. (p, v)
# `part_pair` stands for an (N-1)-way (param, value) combination
# `part_p_pair` stands for an (N-1)-way param combination
# `M` is the number of random cases generated in each iteration.

# Generates every `p_pair` and `pair` for a given `v_count` list.
def generate_pairs(v_count, dim):
    pairs = set()
    p_pairs = []
    for p_pair in itertools.combinations(range(len(v_count)), dim):
        p_pairs.append(p_pair)
    for p_pair in p_pairs:
        v_pairs = itertools.product(*[range(v_count[i]) for i in p_pair])
        for v_pair in v_pairs:
            pair = tuple(zip(p_pair, v_pair))
            pairs.add(pair)
    return p_pairs, pairs


class AETG:

    def __init__(self, v_count: list, dim=2, num_random_cases=50):
        self.v_count = [int(i) for i in v_count]
        self.dim = dim
        self.M = num_random_cases
        self.p_pairs, self.uncovered = generate_pairs(
            self.v_count, dim=self.dim)
        # test cases generated with AETG algorithm
        self.cases = None

    def generate(self):
        if self.cases is not None:
            return self.cases
        cases = []

        # all `p_pair`s for `v_count` & uncovered `pair`s
        p_pairs, uncovered = generate_pairs(self.v_count, dim=self.dim)
        # all `part_p_pair`s & and `part_pair`s
        # used for finding the values of the first N-1 params in each iteration.
        part_p_pairs, part_pairs = generate_pairs(
            self.v_count, dim=self.dim - 1)
        # number of occurrences of every `part_pair` in uncovered `pair`s
        occurrence = dict()
        initial_occurrence = dict()
        for part_p_pair in part_p_pairs:
            initial_occurrence[part_p_pair] = 0
            remaining_params = list(range(len(self.v_count)))
            for p in part_p_pair:
                remaining_params.remove(p)
            initial_occurrence[part_p_pair] += sum(
                [self.v_count[p] for p in remaining_params])
        for part_pair in part_pairs:
            occurrence[part_pair] = initial_occurrence[tuple(
                pv_pair[0] for pv_pair in part_pair)]

        print(len(uncovered), "combinations to cover.")
        qbar = tqdm(total=len(uncovered))
        while len(uncovered):
            # First generate self.M different candidate test cases.
            # Choose a `part_pair` that appears in the greatest number of uncovered pairs
            # for the first (N-1) parameter values
            chosen_part_pair = list(
                max(occurrence.items(), key=lambda x: x[-1])[0])
            chosen_part_pair.sort()
            candidates = []
            for __ in range(self.M):
                # f[] stands for the order in which each param is considered
                f = list(range(len(self.v_count)))
                case = [0] * len(self.v_count)
                # Let f1 = `idx`.
                for i, (idx, val) in enumerate(chosen_part_pair):
                    case[idx] = val
                    f[i], f[idx] = f[idx], f[i]
                # Then choose a random order for the remaining parameters.
                f[self.dim - 1:] = random.sample(f[self.dim - 1:], len(f) - self.dim + 1)
                # For each possible value v for f[j], find the number of new pairs in the set
                # of pairs {f_i_1 = v_i_1, ..., f_i_{N-1} = v_i_{N-1}, f_j = v} where
                # 1 <= i_1 < ... < i_{N-1} < j. Then, let v[j] be one of the values that
                # appeared in the greatest number of new pairs.
                for j, p_j in enumerate(f[self.dim - 1:], self.dim - 1):
                    new_pair_count = [0] * self.v_count[p_j]
                    for v_j in range(self.v_count[p_j]):
                        for part_p_pair in itertools.combinations(f[0:j], self.dim - 1):
                            p_pair = sorted(part_p_pair + (p_j,))
                            pair = tuple(
                                zip(p_pair, (case[p] if p != p_j else v_j for p in p_pair)))
                            if pair in uncovered:
                                new_pair_count[v_j] += 1
                    v_j = new_pair_count.index(max(new_pair_count))
                    case[p_j] = v_j
                if case not in candidates:
                    candidates.append(case)
            # then choose one that covers the most new pairs
            new_pair_count = [0] * len(candidates)
            for i, candidate in enumerate(candidates):
                for p_pair in p_pairs:
                    pair = tuple(zip(p_pair, (candidate[p] for p in p_pair)))
                    if pair in uncovered:
                        new_pair_count[i] += 1
            candidate = candidates[new_pair_count.index(max(new_pair_count))]
            if candidate not in cases:
                cases.append(candidate)
                # update pairs to cover & occurrences of (p, v) in uncovered combinations
                delta = 0
                for p_pair in p_pairs:
                    pair = tuple(zip(p_pair, (candidate[p] for p in p_pair)))
                    if pair in uncovered:
                        delta += 1
                        uncovered.remove(pair)
                        for part_pair in itertools.combinations(pair, self.dim - 1):
                            occurrence[part_pair] -= 1
                qbar.update(delta)
                qbar.set_postfix_str("{} cases generated".format(len(cases)), refresh=True)
        qbar.close()
        print('Done.')
        # cache result
        self.cases = cases
        return cases
