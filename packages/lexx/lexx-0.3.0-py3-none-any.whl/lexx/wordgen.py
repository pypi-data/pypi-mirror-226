
class SoundSystem:
    import re
    rule_re = re.compile(r'([^?!\s]\??!?)', re.UNICODE)

    def __init__(self,
                 phonemes=tuple(),
                 classes=dict(),
                 words=tuple(),
                 filter=None,
                 plugins=tuple(),
                 random_rate=10):
        from .phonemes import PhonemeSet
        self.phonemes = PhonemeSet(phonemes)
        self.randpercent = random_rate
        self.plugins = tuple(plugins)

        from .filter import Filter
        self.filter = filter or Filter()

        from .distribution import make_weighted
        self.classes = {k: make_weighted(v) for k, v in classes.items()}

        self.ruleset = {}
        for (n, word) in enumerate(words):
            # Crude Zipf distribution for word selection.
            self.ruleset[word] = 10.0 / ((n + 1) ** .9)

    # rules allow phonemes to be in the rule, too: CyVN
    def run_rule(self, rule):
        """Generate a single instance of a rule run."""
        from random import randint
        from .errors import RuleError

        parts = self.rule_re.split(rule)[1::2]
        result = []

        for i, part in enumerate(parts):
            # Early-out if it's optional and doesn't make the roll
            if '?' in part and randint(0, 100) >= self.randpercent:
                result.append(None)
                continue

            # Check for '!' and validate it
            nodupe = False
            if '!' in part:
                if part[0] not in self.classes:
                    raise RuleError("Use of '!' here makes no sense: {}".format(rule))
                elif i == 0 or parts[i-1][0] != part[0]:
                    raise RuleError("Misplaced '!' option: in non-duplicate environment: {}.".format(rule))

                # Don't bother de-duping a value that didn't generate
                nodupe = result[-1] is not None

            # Just append a non-class value
            if part[0] not in self.classes:
                result.append(part[0])
                continue

            nph = self.classes[part[0]].select()
            while nodupe and nph == result[-1]:
                nph = self.classes[part[0]].select()
            result.append(nph)

        return "".join([ph for ph in result if ph is not None])

    def apply_plugins(self, word):
        phonemes = self.phonemes.split(word)
        for plug in self.plugins:
            phonemes = plug.apply(phonemes)
        return "".join(phonemes)

    def generate(self, n=10):
        """Generate n unique words randomly from the rules."""
        words = set()
        while len(words) < n:
            from .distribution import select
            rule = select(self.ruleset)
            word = self.run_rule(rule)

            word = self.apply_plugins(word)
            if word == "REJECT":
                continue

            word = self.filter.apply(word)

            if word == "REJECT":
                continue

            words.add(word)

        return list(words)
