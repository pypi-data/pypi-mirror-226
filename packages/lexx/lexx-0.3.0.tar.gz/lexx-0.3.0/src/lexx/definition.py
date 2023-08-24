from lark import Transformer

grammar = r"""
    start:          (statement|comment)+

    statement:        "with" ":" NAME+              -> with
                    | "random-rate" ":" NUMBER      -> randomness
                    | "filter" ":" filter_list      -> filter
                    | "spelling" ":" filter_list    -> spelling
                    | "reject" ":" PHONEME+         -> reject
                    | "words" ":" (MACRO|PHONEME)+  -> words
                    | MACRO "=" PHONEME+            -> macro
                    | CAP "=" PHONEME+              -> class

    filter_list:    filter_item (";" filter_item)* ";"?

    filter_item:      PHONEME ">" PHONEME
                    | PHONEME ">" "!"

    comment:        SH_COMMENT+

    CAP:            ("A".."Z")
    MACRO:          /\$[A-Z]/
    NAME:           /[A-Za-z][A-Za-z0-9_-]*/
    PHONEME:        /[^\t\s=:;!]+/
    WHITESPACE:     (" " | "\n")

    %import common.NUMBER
    %import common.SH_COMMENT
    %import common.WS
    %ignore WS
"""


class DefinitionTransformer(Transformer):
    def filter_list(self, items):
        return items

    def filter_item(self, items):
        match items:
            case (find, repl):
                return (find, repl)
            case (find,):
                return (find, '')

    MACRO = str
    CAP = str
    PHONEME = str
    NAME = str
    NUMBER = int


def load_plugin(name):
    from importlib import import_module
    return import_module(f".{name}", package=f"{__package__}.plugins")


def expand_macros(words, macros):
    from re import sub

    def repl(match):
        return macros.get(match.group(0), "")

    return [sub(r"\$[A-Z]", repl, w) for w in words]


def loads(text):
    from lark import Lark
    from lark.exceptions import UnexpectedInput

    try:
        tree = Lark(grammar).parse(text)
    except UnexpectedInput as ui:
        from .errors import LexxError
        raise LexxError(ui)

    tree = DefinitionTransformer().transform(tree)

    plugins = []
    random_rate = 10
    classes = {}
    macros = {}
    filters = []
    spelling = []
    rejects = []
    words = []
    phonemes = set()

    for c in tree.children:
        match c.data, c.children:
            case 'with', entries:
                plugins.extend(entries)
            case 'randomness', (n,):
                random_rate = n
            case 'filter', (entries,):
                filters.extend(entries)
                phonemes.update(map(lambda x: x[1], entries))
            case 'spelling', (entries,):
                spelling.extend(entries)
            case 'reject', items:
                rejects.extend(items)
            case 'words', entries:
                words += entries
            case 'class', (name, *entries):
                classes[name] = classes.get(name, list()) + entries
                phonemes.update(entries)
            case 'macro', (name, value):
                macros[name] = value
            case other:
                #print("OTHER: ", other)
                pass

    from .filter import Filter
    filt = Filter(replace=filters, reject=rejects)
    spell = Filter(replace=spelling)

    plugins = [load_plugin(n) for n in plugins]

    from .wordgen import SoundSystem
    ssys = SoundSystem(
            phonemes = phonemes,
            classes = classes,
            words = expand_macros(words, macros),
            filter = filt,
            plugins = plugins,
            random_rate = random_rate)

    return ssys, spell


def load(filename):
    with open(filename) as f:
        return loads(f.read())
