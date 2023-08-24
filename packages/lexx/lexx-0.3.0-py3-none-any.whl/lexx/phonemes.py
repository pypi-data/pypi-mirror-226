from collections import namedtuple
Phoneme = namedtuple("Phoneme", ("phoneme", "voiced", "place", "manner"))

class PhonemeSet:
    def __init__(self, phonemes):
        self.phonemes = phonemes

        from re import compile, UNICODE
        split_order = sorted(phonemes, key=len, reverse=True)
        self.__re = compile(f"({'|'.join(split_order)}|.)", UNICODE)

    def __getitem__(self, i):
        return self.phonemes[i]

    def __len__(self):
        return len(self.phonemes)

    def split(self, word):
        return self.__re.split(word)[1::2]


# Phoneme, voiced, location, manner
PHONEMES = {i[0]: Phoneme(*i) for i in [
    # Bilabial, labio-dental
    ('p',  False, 'bilabial',     'stop'),
    ('b',  True,  'bilabial',     'stop'),
    ('ɸ',  False, 'bilabial',     'fricative'),
    ('β',  True,  'bilabial',     'fricative'),
    ('f',  False, 'labiodental',  'fricative'),
    ('v',  True,  'labiodental',  'fricative'),
    ('m',  True,  'bilabial',     'nasal'),
    ('ɱ',  True,  'labiodental',  'nasal'),
    # Alveolar
    ('t',  False, 'alveolar',     'stop'),
    ('d',  True,  'alveolar',     'stop'),
    ('s',  False, 'alveolar',     'sibilant'),
    ('z',  True,  'alveolar',     'sibilant'),
    ('θ',  False, 'alveolar',     'fricative'),
    ('ð',  True,  'alveolar',     'fricative'),
    ('ɬ',  False, 'alveolar',     'lateral fricative'),
    ('ɮ',  True,  'alveolar',     'lateral fricative'),
    ('tɬ', False, 'alveolar',     'lateral affricate'),
    ('dɮ', True,  'alveolar',     'lateral affricate'),
    ('ts', False, 'alveolar',     'affricate'),
    ('dz', True,  'alveolar',     'affricate'),
    ('ʃ',  False, 'postalveolar', 'sibilant'),
    ('ʒ',  True,  'postalveolar', 'sibilant'),
    ('tʃ', False, 'postalveolar', 'affricate'),
    ('dʒ', True,  'postalveolar', 'affricate'),
    ('n',  True,  'alveolar',     'nasal'),
    # Retroflex
    ('ʈ',  False, 'retroflex',    'stop'),
    ('ɖ',  True,  'retroflex',    'stop'),
    ('ʂ',  False, 'retroflex',    'sibilant'),
    ('ʐ',  True,  'retroflex',    'sibilant'),
    ('ʈʂ', False, 'retroflex',    'affricate'),
    ('ɖʐ', True,  'retroflex',    'affricate'),
    ('ɳ',  True,  'retroflex',    'nasal'),
    # Velar
    ('k',  False, 'velar',        'stop'),
    ('g',  True,  'velar',        'stop'),
    ('x',  False, 'velar',        'fricative'),
    ('ɣ',  True,  'velar',        'fricative'),
    ('ŋ',  True,  'velar',        'nasal'),
    # Uvular
    ('q',  False, 'uvular',       'stop'),
    ('ɢ',  True,  'uvular',       'stop'),
    ('χ',  False, 'uvular',       'fricative'),
    ('ʁ',  True,  'uvular',       'fricative'),
    ('ɴ',  True,  'uvular',       'nasal'),
]}


