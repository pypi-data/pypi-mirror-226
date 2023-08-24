from lexx.distribution import WeightedSelector

def test_weighted_selector():
    letters = {'a': 7, 'b': 5, 'c': 1}
    m = WeightedSelector(letters)
    v = {k: 0 for k in letters}
    for i in range(10000):
        c = m.select()
        assert(c in v)
        v[c] += 1

    def check(c1, c2):
        target = letters[c1] / letters[c2]
        ratio = v[c1] / v[c2]
        d = target - ratio
        assert(d <= 0.75 and d >= -0.75)

    check('a', 'c')
    check('b', 'c')
