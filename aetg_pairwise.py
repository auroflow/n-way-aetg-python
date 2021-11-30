from tqdm import tqdm
import random


class AETG:

    def __init__(self, v_count: list, dim=2, num_random_cases=50):
        if dim != 2:
            raise ValueError("Dimension must be 2.")
        # number of possible values of each parameter
        self.v_count = v_count
        # number of random test cases generated in one iteration
        self.M = num_random_cases

        # test cases generated with AETG algorithm
        self.cases = None

    def generate(self):
        if self.cases is not None:
            return self.cases
        cases = []

        # pairs of parameter indices: [(p1, p2), (p1, p3), (p2, p3), ...]
        p_pairs = []
        for i in range(len(self.v_count)):
            for j in range(i + 1, len(self.v_count)):
                p_pairs.append((i, j))
        # pairs to cover. A pair is represented by ((p1, v1), (p2, v2)) where p1 < p2
        uncovered = set()
        # occurrences of (p, v) in uncovered combinations
        occurrence = dict()
        for p1, p2 in p_pairs:
            for v1 in range(self.v_count[p1]):
                for v2 in range(self.v_count[p2]):
                    uncovered.add(((p1, v1), (p2, v2)))
                    occurrence[(p1, v1)] = occurrence.get((p1, v1), 0) + 1
                    occurrence[(p2, v2)] = occurrence.get((p2, v2), 0) + 1

        print(len(uncovered), "combinations to cover.")
        qbar = tqdm(total=len(uncovered))
        while len(uncovered):
            # First generate self.M different candidate test cases.
            # Choose a parameter `idx` and a value `val` for i such that that parameter value
            # appears in the greatest number of uncovered pairs.
            idx, val = max(occurrence, key=occurrence.get)
            candidates = []
            for __ in range(self.M):
                # Let f1 = `idx`. Then choose a random order for the remaining parameters.
                f = list(range(len(self.v_count)))
                f[0], f[idx] = f[idx], f[0]
                f[1:] = random.sample(f[1:], len(f) - 1)
                # For each possible value v for f[j], find the number of new pairs in the set
                # of pairs {f[j] = v and f[i] = v[i] for 1 <= i < j}. Then, let v[j] be one of
                # the values that appeared in the greatest number of new pairs.
                case = [0] * len(self.v_count)
                case[idx] = val
                for j, p_j in enumerate(f[1:], 1):
                    new_pair_count = [0] * self.v_count[p_j]
                    for v_j in range(self.v_count[p_j]):
                        for p_i in f[0:j]:
                            if p_i < p_j:
                                pair = ((p_i, case[p_i]), (p_j, v_j))
                            else:
                                pair = ((p_j, v_j), (p_i, case[p_i]))
                            if pair in uncovered:
                                new_pair_count[v_j] += 1
                    v_j = new_pair_count.index(max(new_pair_count))
                    case[p_j] = v_j
                if case not in candidates:
                    candidates.append(case)
            # then choose one that covers the most new pairs
            new_pair_count = [0] * len(candidates)
            for i, candidate in enumerate(candidates):
                for p_i in range(len(self.v_count)):
                    v_i = candidate[p_i]
                    for p_j in range(p_i + 1, len(self.v_count)):
                        v_j = candidate[p_j]
                        if ((p_i, v_i), (p_j, v_j)) in uncovered:
                            new_pair_count[i] += 1
            candidate = candidates[new_pair_count.index(max(new_pair_count))]
            if candidate not in cases:
                cases.append(candidate)
                # update pairs to cover & occurrences of (p, v) in uncovered combinations
                delta = 0
                for p_i in range(len(self.v_count)):
                    v_i = candidate[p_i]
                    for p_j in range(p_i + 1, len(self.v_count)):
                        v_j = candidate[p_j]
                        if ((p_i, v_i), (p_j, v_j)) in uncovered:
                            delta += 1
                            occurrence[(p_i, v_i)] -= 1
                            occurrence[(p_j, v_j)] -= 1
                            uncovered.remove(((p_i, v_i), (p_j, v_j)))
                qbar.update(delta)
                qbar.set_postfix_str("{} cases generated".format(len(cases)), refresh=True)
        qbar.close()
        print('Done.')
        # cache result
        self.cases = cases
        return cases
