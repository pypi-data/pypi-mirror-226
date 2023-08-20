#!/usr/bin/env python

import sys
import argparse

from pegwords.words import Words
from pegwords.utils import printResult


def printError(expected, result, wordlist):
    print(
        f"Result {result!r} does not match expected {expected!r}!",
        file=sys.stderr,
    )

    maxLen = max(len(expected), len(result))
    match = []
    for index in range(maxLen):
        try:
            expectedLetter = expected[index]
        except IndexError:
            expectedLetter = "-"
        try:
            resultLetter = result[index]
        except IndexError:
            resultLetter = "-"

        match.append(" " if expectedLetter == resultLetter else "|")

    print("EXPECTED:", expected, file=sys.stderr)
    print("         ", "".join(match), file=sys.stderr)
    print("RECEIVED:", result, file=sys.stderr)

    for word, digits in wordlist:
        expectedPrefix = expected[: len(digits)]
        if expectedPrefix != digits:
            print(
                f"For word {word!r}, expected {expectedPrefix!r} but "
                f"the correct value is {digits!r}.",
                file=sys.stderr,
            )
        expected = expected[len(digits) :]


def main():
    parser = argparse.ArgumentParser("Turn a sequence of words into digits")
    parser.add_argument("words", nargs="+", help="The words to convert.")
    parser.add_argument("--expected", help="The expected result.")
    args = parser.parse_args()

    words = Words()
    wordList = []

    for inputWord in args.words:
        wordList.append((inputWord, words.wordToDigits(inputWord)))

    printResult(wordList, "")

    if args.expected:
        result = "".join(digits for (_, digits) in wordList)
        if result != args.expected:
            printError(args.expected, result, wordList)
            sys.exit(1)


if __name__ == "__main__":
    main()
