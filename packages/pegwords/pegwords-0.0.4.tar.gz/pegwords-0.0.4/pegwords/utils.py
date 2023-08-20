def clean(word: str) -> str:
    "Remove non-alpha characters from a string."
    result: list[str] = []
    for letter in word:
        if letter.isalpha():
            result.append(letter)

    return "".join(result)


def dedup(word: str) -> str:
    "De-duplicate repeated letters a string."
    result: list[str] = []
    for letter in word:
        if result:
            if letter != result[-1]:
                result.append(letter)
        else:
            result.append(letter)

    return "".join(result)


def printResult(wordList, remaining):
    resultDigits = []
    resultWords = []

    allDigits = ""
    for word, digits in wordList:
        allDigits += digits
        length = max(len(word), len(digits))
        resultDigits.append(f"{digits:{length}s}")
        resultWords.append(f"{word:{length}s}")

    print(f"{len(allDigits)} digits ({allDigits}) covered by {len(resultWords)} words:")

    print("  DIGITS:", " ".join(resultDigits))
    print("  WORDS: ", " ".join(resultWords))

    if remaining:
        s = "" if len(remaining) == 1 else "s"
        print(f"{len(remaining)} digit{s} remaining:", remaining)
