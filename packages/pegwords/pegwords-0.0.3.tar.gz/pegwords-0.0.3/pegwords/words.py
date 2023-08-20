import sys
import re
from pathlib import Path
from typing import Iterable, Optional, Union

from pegwords.utils import dedup, clean

OPTIONAL = "(a|e|h|i|o|u|w|x|y|th)*"
OPTIONAL_END = re.compile(OPTIONAL + "$")

DIGIT_REGEXPS = [
    re.compile(OPTIONAL + digitRegex)
    for digitRegex in (
        "(c[eiy]|s(?!h)|z)",
        "(t(?!h)|d)+",
        "n+",
        "m+",
        "r+",
        "l+",
        "(j|sh|ch|cz|g(?=e))",
        "(kn?|c[aoku]|g(?!e)?|q|[aeiou]ck?$|c(?=[lnrst])?)",
        "[f|v]+",
        "[b|p]",
    )
]


class Words:
    def __init__(
        self,
        words: Optional[Iterable[str]] = None,
        dictionaryFile: Optional[Union[str, Path]] = None,
        verbose: bool = False,
    ) -> None:
        words = list(words) if words else []

        if dictionaryFile:
            with open(dictionaryFile) as fp:
                for word in fp:
                    words.append(word.strip())

            if verbose:
                print(
                    f"Read {len(words)} words from {str(dictionaryFile)!r}.",
                    file=sys.stderr,
                )

        failCount = 0

        # I don't want to use a defaultdict to hold sets of words for a
        # given string of digits because I don't want empty sets of words
        # to spring into existence.
        numbers: dict[str, set[str]] = {}

        for word in set(map(str.lower, words)):
            try:
                digits = self.wordToDigits(word)
            except ValueError as e:
                failCount += 1
                if verbose:
                    word, suffix = e.args
                    print(
                        f"Failed to convert {word!r} to a number, starting from "
                        f"suffix {suffix!r}.",
                        file=sys.stderr,
                    )
            else:
                try:
                    numbers[digits].add(word)
                except KeyError:
                    numbers[digits] = {word}

        if failCount and verbose:
            print(f"Failed to convert {failCount} words into numbers", file=sys.stderr)

        self.numbers = numbers

    def wordToDigits(self, word: str, verbose: bool = False) -> str:
        """
        Turn a word into a number.
        """
        if verbose:
            print(f"--> Converting {word!r}.", file=sys.stderr)
        index = 0
        result = []
        word = clean(dedup(word))

        while index < len(word):
            suffix = word[index:]
            if verbose:
                print(f"Index {index}, examining: {suffix!r}.", file=sys.stderr)
            for digit, regex in enumerate(DIGIT_REGEXPS):
                match = regex.match(suffix)
                if match:
                    result.append(digit)
                    index += match.end()
                    if verbose:
                        print(
                            f"Matched {regex!r}. Index is now {index}.", file=sys.stderr
                        )
                    break
            else:
                # Fail unless we are at the end of a word with trailing
                # letters not assigned to digits.
                if OPTIONAL_END.match(suffix):
                    break
                else:
                    raise ValueError(word, suffix)

        return "".join(map(str, result))

    def longestPrefix(
        self, digits: str, maxAcceptablePrefix: Optional[int] = None
    ) -> tuple[int, set[str]]:
        """
        Find the set of words matching the longest known prefix of a string of digits.
        """
        if maxAcceptablePrefix is None:
            maxAcceptablePrefix = len(digits)
        origDigits = digits
        digits = digits[:maxAcceptablePrefix]
        while digits:
            if digits in self.numbers:
                return len(digits), self.numbers[digits]
            else:
                digits = digits[:-1]

        raise ValueError(origDigits)

    def __getitem__(self, digits: str) -> set[str]:
        return self.numbers[digits]
