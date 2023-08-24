class Filter:
    def __init__(self, replace=tuple(), reject=tuple()):
        self.replace = replace
        self.reject = reject

    def apply(self, word):
        import re
        for (pat, repl) in self.replace:
            word = re.sub(pat, repl, word)

        for pat in self.reject:
            if re.search(pat, word, flags=re.UNICODE):
                return 'REJECT'

        return word
