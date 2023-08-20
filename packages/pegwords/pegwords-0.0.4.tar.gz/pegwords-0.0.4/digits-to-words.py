#!/usr/bin/env python

import sys
import argparse

from pegwords.words import Words
from pegwords.utils import printResult


def main():
    parser = argparse.ArgumentParser("Turn a digit sequence into mnemonic words")
    parser.add_argument("digits", help="The digits to convert.")
    parser.add_argument(
        "--dictionaryFile",
        default="/usr/share/dict/web2",
        help="A file of dictionary words (one per line).",
    )

    args = parser.parse_args()

    words = Words(dictionaryFile=args.dictionaryFile)

    wordList = []
    digits = args.digits
    maxAcceptablePrefix = None
    printed = False

    while digits:
        prefixLen, candidates = words.longestPrefix(
            digits, maxAcceptablePrefix=maxAcceptablePrefix
        )
        candidates = sorted(candidates)

        if not printed:
            print(
                f"Found {len(candidates)} words covering {prefixLen} "
                f"digits {digits[:prefixLen]!r}:"
            )
            for count, word in enumerate(candidates):
                print(f"  {count}: {word}")
            printed = True

        while True:
            choice = input("Your choice? ")

            if choice == "?":
                printResult(wordList, digits)
                break
            elif choice == "+":
                maxAcceptablePrefix = prefixLen + 1
                printed = False
                break
            elif choice == "-":
                maxAcceptablePrefix = prefixLen - 1
                printed = False
                break
            elif choice == "q":
                sys.exit()
            else:
                try:
                    n = int(choice)
                except ValueError:
                    break
                else:
                    if 0 <= n < len(candidates):
                        wordList.append((candidates[n], digits[:prefixLen]))
                        maxAcceptablePrefix = None
                        digits = digits[prefixLen:]
                        printResult(wordList, digits)
                        printed = False
                        break
                    else:
                        print("Invalid choice.")
                        break


if __name__ == "__main__":
    main()
