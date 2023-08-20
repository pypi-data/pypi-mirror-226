from pegwords.utils import dedup, clean


def testDedupUnchanged():
    assert dedup("hey") == "hey"


def testDedup():
    assert dedup("hheyy") == "hey"


def testCleanUnchanged():
    assert clean("hey") == "hey"


def testClean():
    assert clean("hey you") == "heyyou"
    assert clean("hey+you") == "heyyou"
