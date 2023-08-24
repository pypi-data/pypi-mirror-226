TEST_DEF = """
with: assimilations metathesis
random-rate: 20

#letters: ʔ a á b ch d e g h i k l m n o p r s t u w y

C = t n k m ch l ʔ s r d h w b y p g
D = n l ʔ t k r p
V = ɪ ɛ ʌ ɑ ʊ ɔ

$S = CVD?

words:  V?$S$S V?$S V?$S$S$S

reject: wu yɪ w$ y$ h$ ʔʔ (p|t|k|ʔ)h
filter: nr > tr; mr > pr; ŋ > n

spelling: ɪ > i; ɛ > e; ʌ > a; ɑ > a; ʊ > o; ɔ > au
"""

def test_definition():
    from lexx.definition import loads, load_plugin
    ssys = loads(TEST_DEF)
    classes = dict(
        C = sorted("t n k m ch l ʔ s r d h w b y p g".split()),
        D = sorted("n l ʔ t k r p".split()),
        V = sorted("ɪ ɛ ʌ ɑ ʊ ɔ".split()),
    )
    assert(len(ssys.classes) == len(classes))
    for k, v in classes.items():
        assert(k in ssys.classes)
        assert(sorted(ssys.classes[k]) == v)

    assert(ssys.randpercent == 20)
    assert(ssys.plugins == (load_plugin('assimilations'), load_plugin('metathesis')))

def test_generation():
    from lexx.definition import loads
    ssys = loads(TEST_DEF)

    words = ssys.generate(1000)
    assert(len(words) == 1000)

    import re
    for word in words:
        for r in ssys.filter.reject:
            assert(not re.search(r, word))
        for pat, repl in ssys.filter.replace:
            assert(not re.search(pat, word))
        for pat, repl in ssys.spelling.replace:
            assert(not re.search(pat, word))
