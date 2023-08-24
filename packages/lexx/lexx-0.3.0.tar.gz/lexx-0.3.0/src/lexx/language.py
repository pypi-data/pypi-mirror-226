class Word:
    def __init__(self, spelling, pronunciation):
        self.spelling = spelling
        self.pronunciation = pronunciation

    def __str__(self):
        return self.spelling


class Language:
    def __init__(self, name, root, sounds, spelling):
        self.name = name
        self.root = root
        self.sounds = sounds
        self.spelling = spelling

    def generate(self, count=1):
        return [Word(self.spelling.apply(w), w)
                for w in self.sounds.generate(count)]

    @property
    def definition(self):
        return self.root / f"{self.name}.def"

    @property
    def dictionary(self):
        return self.root / f"{self.name}.csv"
