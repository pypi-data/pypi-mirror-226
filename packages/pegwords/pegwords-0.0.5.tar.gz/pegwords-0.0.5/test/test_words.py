from pegwords.words import Words

wordToDigits = Words().wordToDigits


def testWordlist():
    "Passing a wordlist must work as expected."
    words = Words(["cat", "kid"])
    assert words["71"] == {"cat", "kid"}


def testLeadingZero():
    assert wordToDigits("asteroidal") == "01415"


def testRepeatedLetters():
    assert wordToDigits("nnn") == "2"


def testCat():
    assert wordToDigits("cat") == "71"


def testGeode():
    assert wordToDigits("geode") == "61"


def testWeekday():
    assert wordToDigits("weekday") == "71"


def testWhale():
    assert wordToDigits("whale") == "5"


def testFish():
    assert wordToDigits("fish") == "86"


def testThrush():
    assert wordToDigits("thrush") == "46"


def testHemophobia():
    assert wordToDigits("hemophobia") == "389"


def testPthenB():
    "P then B should be counted as two sounds."
    assert wordToDigits("hipbone") == "992"


def testFthenV():
    "F then V should just count as one sound."
    assert wordToDigits("fv") == "8"


def testStartOfPi():
    "Test the longest prefix from the start of Pi."
    words = Words(["hello", "Jules", "tortilla", "turtle"])
    prefixLen, candidates = words.longestPrefix("14159265")
    assert prefixLen == 4
    assert candidates == {"tortilla", "turtle"}


def testStartOfPiWithMaxPrefix():
    "Test the longest prefix from the start of Pi, with a maximum prefix length."
    words = Words(["hello", "Jules", "tortilla", "tire"])
    prefixLen, candidates = words.longestPrefix("14159265", maxAcceptablePrefix=2)
    assert prefixLen == 2
    assert candidates == {"tire"}
