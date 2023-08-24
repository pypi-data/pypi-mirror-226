
# When you are selecting from a pool a *lot*, this
# will speed things up a bit.  Takes a dict of keys
# and weights.
class WeightedSelector(object):
    def __init__(self, dic):
        # build parallel arrays for indexing
        self.keys = list(dic.keys())
        self.weights = [dic[k] for k in self.keys]
        self.sum = sum(self.weights)
        self.n = len(self.keys)

    def select(self):
        from random import uniform
        pick = uniform(0, self.sum)
        tmp = 0
        for i in range(self.n):
            tmp += self.weights[i]
            if pick < tmp:
                return self.keys[i]

    def __iter__(self):
        return iter(self.keys)


# Weighted random selection.
def select(dic):
    from random import uniform
    total = sum(dic.values())
    pick = uniform(0, total-1)
    tmp = 0
    for key, weight in dic.items():
        tmp += weight
        if pick < tmp:
            return key


# Give approximately natural frequencies to phonemes.
# Gusein-Zade law.
def jitter(v, percent=10.0):
    from random import random
    move = v * (percent / 100.0)
    return v + (random() * move) - (move / 2)


# Takes a list of phonemes, returns a string
# in the form expected by SoundSystem.add_ph_unit().
def natural_weights(phonemes):
    import math
    n = len(phonemes)
    weighted = {}
    for i in range(n):
        weighted[phonemes[i]] = jitter((math.log(n + 1) - math.log(i + 1)) / n)
    return [f'{p}:{v:.2f}' for p, v in weighted.items()]


def list_to_weighted(items):
    def parse(s):
        if ':' not in s:
            from .errors import RuleError
            raise RuleError(f'{s} not a valid phoneme and weight')
        ph, w = s.split(":", maxsplit=1)
        return ph, float(w)
    return dict([parse(s) for s in items])


# Make a WeightedSelector by adding natural weights
# if there's no weighting.
def make_weighted(items):
    if ':' not in "".join(items):
        items = natural_weights(items)
    return WeightedSelector(list_to_weighted(items))
