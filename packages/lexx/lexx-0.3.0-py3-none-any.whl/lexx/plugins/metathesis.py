from ..phonemes import PHONEMES

def coronal_metathesis(g1, g2):
    ph1 = PHONEMES.get(g1)
    ph2 = PHONEMES.get(g2)

    if not (ph1 and ph2):
        return g1, g2

    if ph1.place == 'alveolar' and \
       ph1.manner == ph2.manner and \
       ph2.place in ('velar', 'bilabial') and \
       ph2.manner in ('stop', 'nasal'):
        return g2, g1

    return g1, g2


def apply(word):
    new = word[:]
    for i in range(len(word) - 1):
        new[i], new[i+1] = coronal_metathesis(word[i], word[i+1])
    return new
