# SPDX-FileCopyrightText: 2023-present Justin C. Miller <pypi@justin.cm>
#
# SPDX-License-Identifier: MIT
import click

from lexx.__about__ import __version__

class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the full command name
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args

@click.command(cls=AliasedGroup, context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="lexx")
@click.option("-l", "--lang", required=True, help="Name of the language to use")
@click.option("-r", "--root", default=".", help="Path where language files are located")
@click.pass_context
def lexx(ctx, lang, root):
    from pathlib import Path
    root = Path(root)
    file = root / f"{lang}.def"

    from ..definition import load
    from ..language import Language
    from ..errors import LexxError
    try:
        ssys, spell = load(file)
        ctx.obj = Language(lang, root, ssys, spell)
    except LexxError as e:
        from sys import stderr
        print(f"ERROR: {e}", file=stderr)
        exit(1)

@lexx.command
@click.pass_obj
@click.option("-n", "--number", type=int, default=10, help="Number of words to generate")
@click.option("-o", "--one-per-line", is_flag=True, default=False, help="Show one word per line")
def generate(lang, number, one_per_line):
    """Generate random words."""
    words = lang.generate(number)
    if one_per_line:
        lines = [f"{w.spelling:15} /{w.pronunciation}/" for w in words]
    else:
        from textwrap import wrap
        lines = wrap(" ".join([w.spelling for w in words]), 70)

    print("\n".join(lines))


@lexx.command
@click.pass_obj
@click.option("-n", "--number", type=int, default=10, help="Number of sentences to generate")
def paragraph(lang, number):
    """Generate a fake paragraph of text."""
    from random import randint

    sentences = []

    for i in range(number):
        word_count = randint(3, 11)
        words = []

        words.append(lang.generate(1)[0].spelling.capitalize())
        words.extend([w.spelling for w in lang.generate(word_count)])

        if word_count >= 7:
            i = randint(0, word_count - 2)
            words[i] += ","

        if randint(0, 100) <= 85:
            words[-1] += "."
        else:
            words[-1] += "?"

        sentences.append(" ".join(words))

    from textwrap import wrap
    print("\n".join(wrap(" ".join(sentences), 70)))


@lexx.command
@click.pass_obj
@click.option("-n", "--number", type=int, default=10, help="Number of word options to generate")
def add(lang, number):
    """Add new words to the lexicon."""
    words = lang.generate(number)
    lines = [f"{w.spelling},/{w.pronunciation}/,pos.,definition" for w in words]

    from editor import editor
    additions = editor(text="\n".join(sorted(lines)))
    if not additions.strip():
        print("No additions made.")
        return

    entries = []
    from os.path import exists
    if exists(lang.dictionary):
        with open(lang.dictionary) as f:
            entries = [l.strip() for l in f.readlines()]

    newdict = f"{lang.dictionary}.new"
    entries = sorted(entries + additions.split("\n"))
    with open(newdict, "w") as f:
        print("\n".join([e for e in entries if e]), file=f)

    from os import rename
    rename(newdict, lang.dictionary)
