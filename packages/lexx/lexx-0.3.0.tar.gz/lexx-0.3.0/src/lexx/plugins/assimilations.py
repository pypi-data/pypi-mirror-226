from ..phonemes import PHONEMES

def nasal_assimilate(g1, g2):
    ph1 = PHONEMES.get(g1)
    ph2 = PHONEMES.get(g2)

    if not (ph1 and ph2):
        return g1

    if ph1.manner != 'nasal':
        return g1

    for ph in PHONEMES.values():
        if ph.manner == 'nasal' and ph.place == ph2.place:
            return ph.phoneme

    return g1


def voice_assimilate(g1, g2):
    ph1 = PHONEMES.get(g1)
    ph2 = PHONEMES.get(g2)

    if not (ph1 and ph2):
        return g1

    if ph2.manner != 'nasal':
        return g1

    for ph in PHONEMES.values():
        if ph.place == ph1.place and \
           ph.manner == ph1.manner and \
           ph.voiced == ph2.voiced:
            return ph.phoneme

    return g1


def apply(word):
    new = word[:]
    for i in range(len(word) - 1):
        new[i] = voice_assimilate(word[i], word[i+1])
        new[i] = nasal_assimilate(new[i], word[i+1])
    return new
